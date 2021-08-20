# ansible-robonomics-network
Ansible playbooks for Robonomics network management.

## Requirements
- Ansible: https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html

## Usage
### Robonomics collator role
- Launch Robonomics main collator:

  ``` ansible-playbook -i inventory.ini collators-Earth.yml ```

- Remove Robonomics main collator:

  ``` ansible-playbook -i inventory.ini collators-Earth.yml -t remove ```

- Stop Robonomics main collator service:

  ``` ansible-playbook -i inventory.ini collators-Earth.yml -t stop_service ```

- Start Robonomics main collator service:

  ``` ansible-playbook -i inventory.ini collators-Earth.yml -t start_service ```

- Restart Robonomics main collator service:

  ``` ansible-playbook -i inventory.ini collators-Earth.yml -t restart_service ```

- Update Robonomics main collator service and start it:

  ``` ansible-playbook -i inventory.ini collators-Earth.yml -t set_service -t start_service ```
