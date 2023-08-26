zjleblanc.reporting.facts
=========

Generate a report using device facts

Galaxy Tags: \[ report facts html \]

Required Variables
------------------

| Name | Example | Description |
| -------- | ------- | ------------------- |
| facts_table_limit | ["ansible_fips", "ansible_domain"] | limit facts in report |
| facts_table_limit_prefix | ansible_net_ | limit facts in report to vars starting with prefix |
| facts_table_exclude | ["ansible_nonsense", "ansible_confusion"] | exclude facts in report |
| facts_table_exclude_prefix | ansible_net_ | exclude facts staring with prefix in report |
| table_output_remote_host | report_server | inventory host to copy report to |


Role Variables
--------------

| Variable | Type | Value or Expression | Description |
| -------- | ------- | ------------------- | --------- |
| facts_table_title | default | Auto-generated Report |  |
| facts_table_timestamp | default | {{ lookup('pipe', 'date +"%Y-%m-%d @ %H:%M:%S"') }} |  |
| facts_table_output_dest | default | {{ playbook_dir }}/zjleblanc.table.html | will be local or remote based on `table_output_remote_host` |
| facts_table_data | var | {{ hostvars }} | change at your own risk :O |
| facts_table_data_list | var | {{ facts_table_data | json_query('*') }} |  |
| facts_table_data_model | var | {{ facts_table_data_list[0] }} |  |
| facts_table_data_header_filters | var | {'limit': '{{ facts_table_limit | default([]) ... |  |
| facts_table_data_headers | var | {{ facts_table_data_model | ... |  |

Resolving Headers
-----------------

Users can determine the set of table headers via the limit/exclude variables. Dictionaries and lists will not be traversed, so they are always excluded from the table. The rules are processed in the following order:

| Order | Rule | Outcome |
| :---: | --- | :---: |
| 1 | Fact name in `facts_table_limit` list | Included |
| 2 | Fact name starts with `facts_table_limit_prefix` | Included |
| 3 | Fact name in `facts_table_exclude` list | Excluded |
| 4 | Fact name starts with `facts_table_exclude_prefix` | Excluded |
| 5 | No `facts_table_limit` or `facts_table_limit_prefix` provided | Included |

Example Playbook
----------------

```yaml
---
- hosts: all
  gather_facts: true

  tasks:
    - name: Limit to vars starting with ansible_
      run_once: true
      ansible.builtin.include_role:
        name: zjleblanc.reporting.facts
      vars:
        facts_table_title: "Facts Example"
        facts_table_limit_prefix: ansible_
        facts_table_output_dest: "{{ playbook_dir }}/zjleblanc.facts.html"
```

License
-------

license (GPL-2.0-or-later, MIT, etc)

Author Information
-------
**Zachary LeBlanc**

Red Hat