zjleblanc.reporting.org_host_metrics
=========

Generate a report of Ansible host entitlement usage stratified by Organization. Purpose-built to work with the data model produced by the [zjleblanc.utils.org_host_metrics](https://galaxy.ansible.com/ui/repo/published/zjleblanc/utils/content/lookup/org_host_metrics/) lookup plugin.

[Issue Tracker](https://github.com/zjleblanc/zjleblanc.reporting/issues)

Minimum Ansible Version: 2.9

Galaxy Tags: \[ report organization host metrics html utils analytics \]

Expected Variables
------------------

| Name | Example | Description |
| -------- | ------- | ------------------- |
| org_host_metrics_remote_host | report_server | inventory host to copy report to (otherwise writes to localhost) |

Role Variables
--------------

| Variable | Type | Value or Expression | Description |
| -------- | ------- | ------------------- | --------- |
| org_host_metrics_title | default | Organization Host Metrics Report |  |
| org_host_metrics_desc | default | Ansible host entitlement usage report ... |  |
| org_host_metrics_timestamp | default | {{ lookup('pipe', 'date +"%Y-%m-%d @ %H:%M:%S"') }} |  |
| org_host_metrics_output_dest | default | {{ playbook_dir }}/zjleblanc.org_host_metrics.html | report html file destination |
| org_host_metrics_data | var | {{ lookup('zjleblanc.utils.org_host_metrics') }} | See [data model](https://galaxy.ansible.com/ui/repo/published/zjleblanc/utils/content/lookup/org_host_metrics/#return-values) |

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

  ```yaml
    - hosts: localhost
      tasks:
        - name: Execute org_host_metrics role
          ansible.builtin.include_role:
            name: zjleblanc.reporting.org_host_metrics
          vars:
            org_host_metrics: "{{ lookup('zjleblanc.utils.org_host_metrics') }}"
  ```

License
-------

GPL-3.0-only

Author Information
-------
**Zachary LeBlanc**

Red Hat
