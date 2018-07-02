#!/usr/bin/env python

'''
Dynamic inventory of libvirt script for Ansible, in Python.
'''

import sys
import argparse
import libvirt
import json
import os

class LibvirtInventory(object):

    def __init__(self):
        self.args       = None
        self.read_cli_args()

        self.inventory  = {'_meta': {'hostvars': {}}}
        self.driver     = os.getenv('LIBVIRT_DRIVER',       default='qemu')
        self.transport  = os.getenv('LIBVIRT_TRANSPORT',    default='ssh')
        self.username   = os.getenv('LIBVIRT_USER',         default='root')
        self.hostname   = os.getenv('LIBVIRT_HOST',         default='localhost')
        self.url        = os.getenv('LIBVIRT_URL',          default='system')
        self.uri        = '{}+{}:\/\/{}\@{}\/{}'.format(    self.driver,
                                                        self.transport,
                                                        self.username,
                                                        self.hostname,
                                                        self.url
                                                    )

        # Data to print
        if self.args.host:
            inventory_data = self.host_info()
        elif self.args.list:
            inventory_data = self.inv_info()

        print(inventory_data)

    @property
    def conn(self):
        try:
            conn = libvirt.open(self.uri)
        except libvirtError as e:
            err_msg = "Error: {}, Traceback: {}".format(e, traceback.format_exc())
            sys.stderr.write(err_msg)
        else:
            return conn

    def parse_cli_args(self):
        ''' Command line argument processing '''

        parser = argparse.ArgumentParser(description='Libvirt Ansible Inventory')
        parser.add_argument('--list', action='store_true', default=True,
                            help='List instances (default: True)')
        parser.add_argument('--host', action='store',
                            help='Get all the variables about a specific instance')
        self.args = parser.parse_args()

    def find_vm(self, vmid):
        """
        Extra bonus feature: vmid = -1 returns a list of everything
        """
        vms = []

        # this block of code borrowed from virt-manager:
        # get working domain's name
        ids = self.conn.listDomainsID()
        for id in ids:
            vm = self.conn.lookupByID(id)
            vms.append(vm)
        # get defined domain
        names = self.conn.listDefinedDomains()
        for name in names:
            vm = self.conn.lookupByName(name)
            vms.append(vm)

        if vmid == -1:
            return vms

        for vm in vms:
            if vm.name() == vmid:
                return vm

    @property
    def inv_info(self):
        try:
            vms = self.find_vm(-1)
        except libvirtError:
        if len(vms) == 0:
            return
        else:
            for vm in vms:
                self.vm_info(vm)

    @property
    def host_info(self):
        self.dom_info(self.host)

    def vm_info(self, dom):
        try:
            domain = find_vm(dom)
            dom_inv = json.loads(domain.metadata(0, None))
        except (ValueError,libvirt.libvirtError):
            dom_inv = {}
        else:
            try:
                dom_host_vars = {}
                dom_ifaces = domain.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT)
                if dom_ifaces != None:
                    for iface in dom_ifaces:
                        if iface == 'lo':
                            continue
                        for addr in dom_ifaces[iface]['addrs']:
                            if addr['type'] == 0:
                                dom_host_vars['ansible_host'] =  addr['addr']
                if 'ansible_host' not in dom_host_vars:
                    return
                if 'groups' in dom_inv:
                    for group in dom_inv['groups']:
                        if group in self.inventory:
                            self.inventory[group]['hosts'].append(domain.name())
                        else:
                            self.inventory.update({group: {'hosts': [domain.name()]}})
                dom_host_vars['ansible_user'] = 'root'
                if 'hostvars' in dom_inv:
                    dom_host_vars.update(dom_inv['hostvars'])
                self.inventory['_meta']['hostvars'].update({domain.name(): dom_host_vars })
            except (TypeError,libvirt.libvirtError):
                pass

if __name__ == '__main__':
    # Run the script
    LibvirtInventory()
