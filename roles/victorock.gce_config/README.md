# Ansible Role: Google Compute Engine

Configure Google Compute Engine

Cloud Provider:
```YAML
cloud_provider:
  provider: "gce"
  region: "europe-west1"
  zone: "europe-west1-d"
  project: "darkbulb-lab"
```

Cloud Compute Instance:
```YAML
cloud_compute:
  instance:
    jenkins-devops-victorock-io-000:
      name: jenkins-devops-victorock-io-000
      size: n1-standard-1
      image: centos-7
      credential:
        username: jdacosta
        key: jenkins-devops-victorock-io
      network:
        subnet: devops-victorock-io
        public: ephemeral
      tags:
        - jenkins
```

Cloud Network Subnet:
```YAML
cloud_network:
  subnet:
    devops-victorock-io:
      name: devops-victorock-io
      cidr: "10.1.1.0/24"
```

Cloud Network Firewall:
```YAML
cloud_network:
  firewall:
    devops-victorock-io-ssh-all:
      name: devops-victorock-io-ssh-all
      subnet: devops-victorock-io
      src_cidr: 0.0.0.0/0
      dst_port: 22
      proto: tcp

    devops-victorock-io-http-all:
      name: devops-victorock-io-http-all
      subnet: devops-victorock-io
      src_cidr: 0.0.0.0/0
      dst_port: 22
      proto: tcp

    devops-victorock-io-https-all:
      name: devops-victorock-io-https-all
      subnet: devops-victorock-io
      src_cidr: 0.0.0.0/0
      dst_port: 443
      proto: tcp

    devops-victorock-io-icmp-all:
      name: devops-victorock-io-icmp-all
      subnet: devops-victorock-io
      src_cidr: 0.0.0.0/0
      proto: icmp
```

Cloud Network Public:
```YAML
cloud_network:
  public:
    jenkins-devops-victorock-io:
      name: jenkins-devops-victorock-io
```

Cloud Network Public:
```YAML
cloud_network:
  loadbalance:
    http-jenkins-devops-victorock-io:
      name: http-jenkins-devops-victorock-io
      # Reference to Public Name
      public: jenkins-devops-victorock-io
      protocol: tcp
      port: 80
      members:
        # Reference to Instance
        - jenkins-devops-victorock-io-000
      healthcheck:
        name: http-jenkins-devops-victorock-io
        type: HTTP
        port: 80
        protocol: tcp
        url: "/"
    https-jenkins-devops-victorock-io:
      name: https-jenkins-devops-victorock-io
      public: jenkins-devops-victorock-io
      protocol: tcp
      port: 443
      members:
        # Reference to Instance Name
        - jenkins-devops-victorock-io-000
      healthcheck:
        name: https-jenkins-devops-victorock-io
        type: HTTPS
        port: 443
        protocol: tcp
        url: "/"
```

Cloud Network DNS:
```YAML
cloud_network:
  dns:
    jenkins-devops-victorock-io:
      name: jenkins-devops-victorock-io
      # Reference to Public Name
      public: jenkins-devops-victorock-io
      zone: devops.victorock.io
      record: jenkins.devops.victorock.io
```

## Example

Playbook: Instance Provisioning

```YAML
---
- name: "Provision: Google Compute Engine"
  hosts: localhost
  connection: local
  gather_facts: false
  become: false

  tasks:
    - name: "victorock.gce_config"
      include_role:
        name: victorock.gce_config
        tasks_from: compute
      vars:
        cloud_compute:
          instance:
            jenkins-devops-victorock-io-000:
              name: jenkins-devops-victorock-io-000
              size: n1-standard-1
              image: centos-7
              credential:
                username: jdacosta
                key: jenkins-devops-victorock-io
```

## License

GPLv3

## Author Information

Victor da Costa
