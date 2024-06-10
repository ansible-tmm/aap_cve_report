zjleblanc.reporting.dnf
=========

Generate a report using linux patch results with pre-check information

[Issue Tracker](https://github.com/zjleblanc/zjleblanc.reporting/issues)

Minimum Ansible Version: 2.9

Galaxy Tags: \[ report linux patch html tools \]

Required Variables
------------------

| Name | Example | Description |
| -------- | ------- | ------------------- |
| linux_patch_output_remote_host | report_server | inventory host to copy report to |


Role Variables
--------------

| Variable | Type | Value or Expression | Description |
| -------- | ------- | ------------------- | --------- |
| linux_patch_title | default | Ansible dnf Patch Report | report title |
| linux_patch_desc | default | Ansible dnf (or yum) patching report with pre ... | report description |
| linux_patch_timestamp | default | {{ lookup('pipe', 'date +"%Y-%m-%d @ %H:%M:%S"') }} | report timestamp |
| linux_patch_output_dest | default | {{ playbook_dir }}/zjleblanc.reporting.dnf.html | report html file destination |
| linux_patch_hosts | default | {{ ansible_play_hosts }} |  |
| linux_patch_text_success | default | #204d00 | 204d00" |
| linux_patch_text_danger | default | #5f0000 | 5f0000" |
| linux_patch_text_header | default | #147878 | 147878" |
| linux_patch_host_fact_cards | default | [{'var': 'inventory_hostname'}, {'var': ... |  |

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

  ```yaml
    - hosts: servers
      tasks:
        - name: Execute dnf role
          ansible.builtin.include_role:
            name: dnf
          vars:
            linux_patch_output_remote_host: report_server
  ```

License
-------

GPL-3.0-only

Author Information
-------
**Zachary LeBlanc**

Red Hat
