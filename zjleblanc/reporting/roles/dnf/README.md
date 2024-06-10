zjleblanc.reporting.dnf
=========

Generate a report using linux patch results with pre-check information

[Issue Tracker](https://github.com/zjleblanc/zjleblanc.reporting/issues)

Minimum Ansible Version: 2.9

Galaxy Tags: \[ report linux patch html tools \]

Required Hostvars
------------------

These should be set prior to invoking the role with `ansible.builtin.set_fact`. (See example playbook)

| Name | Description |
| ---- | ----------- |
| pre_check_services | Output of `ansible.builtin.service_facts` before patch operation |
| services | Output of `ansible.builtin.service_facts` after patch operation |
| pkg_mgr_output | Output of `ansible.builtin.dnf` (or yum) |


Role Variables
--------------

| Variable | Type | Value or Expression | Description |
| -------- | ------- | ------------------- | --------- |
| linux_patch_title | default | Ansible dnf Patch Report | report title |
| linux_patch_desc | default | Ansible dnf (or yum) patching report with pre ... | report description |
| linux_patch_timestamp | default | {{ lookup('pipe', 'date +"%Y-%m-%d @ %H:%M:%S"') }} | report timestamp |
| linux_patch_output_dest | default | {{ playbook_dir }}/zjleblanc.reporting.dnf.html | report html file destination |
| linux_patch_output_remote_host | default | {{ report_server \| default('localhost') }} | inventory host to copy report to |
| linux_patch_hosts | default | {{ linux_patch_run_once \| ternary(ansible_play_hosts, \[inventory_hostname\]) }} | hosts to include in the report  |
| linux_patch_text_success | default | #204d00 | success text color |
| linux_patch_text_danger | default | #5f0000 | danger text color |
| linux_patch_text_header | default | #147878 | header text color |
| linux_patch_host_fact_cards | default | \[{'var': 'inventory_hostname'}, {'var': ... | customizable list of host fact cards |

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

  ```yaml
    - name: Example playbook to patch and generate report
      hosts:
        - rhel
        - fedora
      become: true

      tasks:
        - name: Get services
          check_mode: false
          ansible.builtin.service_facts:

        - name: Pre-check | services state
          ansible.builtin.set_fact:
            pre_check_services: "{{ services }}"

        - name: Upgrade packages (dnf)
          when: ansible_pkg_mgr == "dnf"
          block:
            - name: Patch (dnf)
              register: r_patch_dnf
              ansible.builtin.dnf:
                name: '*'
                state: latest
                exclude: "{{ exclude_packages }}"
                disable_gpg_check: true

            - name: Set fact for report
              ansible.builtin.set_fact:
                pkg_mgr_output: "{{ r_patch_dnf }}"

        - name: Upgrade packages (yum)
          when: ansible_pkg_mgr == "yum"
          block:
            - name: Patch (yum)
              register: r_patch_yum
              ansible.builtin.yum:
                name: '*'
                state: latest
                exclude: "{{ exclude_packages }}"
                disable_gpg_check: true

            - name: Set fact for report
              ansible.builtin.set_fact:
                pkg_mgr_output: "{{ r_patch_yum }}"

        - name: Check to see if we need a reboot
          register: r_reboot
          check_mode: false
          ansible.builtin.command: needs-restarting -r
          changed_when: result.rc == 1
          failed_when: result.rc > 1

        - name: Reboot Server if Necessary
          ansible.builtin.reboot:
          when: r_reboot.rc == 1

        - name: Get services
          check_mode: false
          ansible.builtin.service_facts:

        - name: Generate report
          ansible.builtin.include_role:
            name: zjleblanc.reporting.dnf
          vars:
            linux_patch_output_remote_host: my_report_server_inventory_hostname

            ### per host suggestions ###
            ### parameterize the report dest OR the host dest ###
            # linux_patch_run_once: false
            # linux_patch_output_dest: "/var/www/html/{{ inventory_hostname}}.report.html"
            # linux_patch_output_remote_host: "{{ inventory_hostname }}"
  ```

License
-------

GPL-3.0-only

Author Information
-------
**Zachary LeBlanc**

Red Hat
