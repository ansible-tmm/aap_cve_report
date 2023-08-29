zjleblanc.reporting.table
=========

Generate a tabular HTML report
[View Example 📈](https://reports.autodotes.com/roles/table.mlb.html)

Galaxy Tags: \[ report table html \]

Required Variables
------------------

| Name | Example | Description |
| -------- | ------- | ------------------- |
| table_data | list[list] OR list[dict] | tabular data used in report |
| table_output_remote_host | report_server | inventory host to copy report to |


Role Variables
--------------

| Variable | Type | Value or Expression | Description |
| -------- | ------- | ------------------- | --------- |
| table_title | default | Auto-generated Report |  |
| table_timestamp | default | {{ lookup('pipe', 'date +"%Y-%m-%d @ %H:%M:%S"') }} |  |
| table_data_type | default | dict | type of input data ([see examples](#choosing-data-type)) |
| table_headers | ["First Name", "Last Name", "Birthday"] | optionally provide column headers |
| table_first_row_headers | default | False | flag for headers in the first row |
| table_output_dest | default | {{ playbook_dir }}/zjleblanc.table.html |  |

Choosing Data Type
------------------

When the input data is a list of objects, use **table_data_type: dict**. Example data below:
```json
[
  {
    "First Name": "Zach",
    "Last Name": "LeBlanc",
    "Birthday": "annual"
  },
  {
    "First Name": "Linux",
    "Last Name": "Machines",
    "Birthday": "1/1/1970"
  },
  ...
]
```

When the input data is a list of lists, use **table_data_type: list**. Example data below:
```json
[
  ["Zach", "LeBlanc", "annual"],
  ["Linux", "Machines", "1/1/1970"],
  ...
]
```

Examples
--------

```yaml
  - name: Inferring headers from dictionary data
    hosts: servers
    tasks:
      - name: Infer headers from dictionary data
        ansible.builtin.include_role:
          name: zjleblanc.reporting.table
        vars:
          table_data:
            - "First Name": Zach
              "Last Name": LeBlanc
              "Birthday": annual:)
            - "First Name": Linux
              "Last Name": Machines
              "Birthday": 1/1/1970
          table_data_type: dict
          table_output_remote_host: report_server
          table_output_dest: "{{ reports_dir }}/table.html"

      - name: Provide separate headers for list data
        ansible.builtin.include_role:
          name: zjleblanc.reporting.table
        vars:
          table_data:
            - ["Zach", "LeBlanc", "annual:)"]
            - ["Linux", "Machines", "1/1/1970"]
          table_data_type: list
          table_headers: ["First Name", "Last Name", "Birthday"]
          table_output_remote_host: report_server
          table_output_dest: "{{ reports_dir }}/table.html"

      - name: Provide list data with headers in the first row
        ansible.builtin.include_role:
          name: zjleblanc.reporting.table
        vars:
          table_data:
            - ["First Name", "Last Name", "Birthday"]
            - ["Zach", "LeBlanc", "annual:)"]
            - ["Linux", "Machines", "1/1/1970"]
          table_data_type: list
          table_first_row_headers: true
          table_output_remote_host: report_server
          table_output_dest: "{{ reports_dir }}/table.html"
```

License
-------

license (GPL-2.0-or-later, MIT, etc)

Author Information
-------
**Zachary LeBlanc**

Red Hat
