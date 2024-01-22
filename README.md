# ansible-robonomics-network
Ansible playbooks for Robonomics networks management.

## Requirements
- Ansible: https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

## Usage
### Example

- Execute 01_Common.yml tags for specified inventory and hosts:

  ``` ansible-playbook -i path/to/inventory/file ./01_Common.yml -l collators[2] -t tag1,tag3```

- Get all tags available in the playbook:

  ``` ansible-playbook 02_Parachain.yml --list-tags ```
