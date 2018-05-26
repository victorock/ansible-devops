# Ansible Role: Linux

Configure Baseline

```
linux_hostname - System Hostname (string)
linux_update - Update (ALL) System Packages (bool)
linux_packages - OS Specific packages (list)
linux_repos - OS Specific repositories (list of hashes)
linux_rhs - System Registration to RHS (bool)
linux_rhs_repos - RHS Specific repositories (list)
linux_rhs_org_id - RHS Specific organisation id (string)
linux_rhs_activationkey - RHS Specific activation key (string)
linux_rhs_autosubscribe - RHS Specific autosubscribe (bool)

```

## Example

Playbook: Configure System

```YAML
---
- name: "Linux: Configure System"
  hosts: linux
  gather_facts: true
  become: true

  tasks:
    - name: "victorock.linux"
      include_role:
        name: victorock.linux
        tasks_from: run
      vars:
        linux_update: yes

```

## License

GPLv3

## Author Information

Victor da Costa
