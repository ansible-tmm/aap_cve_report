#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: Zachary LeBlanc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, annotations, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: cve_info
author: "Zach LeBlanc (@zjleblanc)"
short_description: Update Favorite Movies for a TMDB account
description:
  - This module gets movies favorited by a specified TMDB account
options:
  ids:
    description:
      - CVEs for Ids
    type: list
    elements: str
    required: false
    version_added: "1.5.0"
  severity:
    description:
      - severity filter
    type: list
    elements: str
    default:
      - important
      - moderate
      - low
    required: false
    version_added: "1.5.0"
  package:
    description:
      - package filter
    type: list
    elements: str
    required: false
    version_added: "1.5.0"
  product:
    description:
      - product filter (supports Perl compatible regular expressions)
    type: list
    elements: str
    required: false
    version_added: "1.5.0"
  details:
    description:
      - get cve details or return metadata
    type: bool
    required: false
    default: true
    version_added: "1.5.0"
attributes:
  platform:
    platforms: all
"""

EXAMPLES = r"""
- name: Get by CVE ids
  zjleblanc.reporting.cve_info:
    ids:
      - CVE-2015-0209
      - CVE-2015-0206
      - CVE-2015-0205

- name: Get by severity
  zjleblanc.reporting.cve_info:
    severity:
      - important

- name: Get by product affected
  zjleblanc.reporting.cve_info:
    product:
      - Red Hat Ansible Automation Platform 2

- name: Get by package affected
  zjleblanc.reporting.cve_info:
    package:
      - automation-gateway
"""

RETURN = r"""
cves:
  description: List of CVEs
  returned: success
  type: dict
  sample:
    important:
      - threat_severity: Low
        public_date: '2015-05-22T00:00:00Z'
        bugzilla:
          description: 'postgresql: unanticipated errors from the standard library'
          id: '1221539'
          url: https://bugzilla.redhat.com/show_bug.cgi?id=1221539
        cvss:
          cvss_base_score: '4.0'
          cvss_scoring_vector: AV:N/AC:H/Au:N/C:P/I:N/A:P
          status: verified
        cwe: CWE-391
        details:
          - The snprintf implementation in PostgreSQL before 9.0.20, 9.1.x before 9.1.16, 9.2.x
            before 9.2.11, 9.3.x before 9.3.7, and 9.4.x before 9.4.2 does not properly handle
            system-call errors, which allows attackers to obtain sensitive information or have
            other unspecified impact via unknown vectors, as demonstrated by an out-of-memory
            error.
          - It was discovered that PostgreSQL did not properly check the return values of certain
            standard library functions. If the system was in a state that would cause the standard
            library functions to fail (for example, memory exhaustion), an authenticated user
            could possibly exploit this flaw to disclose partial memory contents or cause the
            GSSAPI authentication to use an incorrect keytab file.
        statement: 'Red Hat Enterprise Linux 5 is now in Production 3 Phase of the support
          and maintenance life cycle. This flaw has been rated as having Low security impact
          and is not currently planned to be addressed in future updates. For additional information,
          refer to the Red Hat Enterprise Linux Life Cycle: https://access.redhat.com/support/policy/updates/errata/.'
        acknowledgement: Red Hat would like to thank PostgreSQL project for reporting this
          issue. Upstream acknowledges Noah Misch as the original reporter.
        affected_release:
          - product_name: Red Hat Enterprise Linux 6
            release_date: '2015-06-29T00:00:00Z'
            advisory: RHSA-2015:1194
            cpe: cpe:/o:redhat:enterprise_linux:6
            package: postgresql-0:8.4.20-3.el6_6
        upstream_fix: postgresql 9.4.2, postgresql 9.3.7, postgresql 9.2.11, postgresql 9.1.16, postgresql 9.0.20
        references:
          - https://nvd.nist.gov/vuln/detail/CVE-2015-3166
        name: CVE-2015-3166
        csaw: false
    moderate: {}
    low: {}
not_found:
  description: List of CVEs not found
  returned: success
  type: list
  elements: str
  sample:
    - CVE-000-1111
    - CVE-222-3333
"""

from ansible.module_utils.basic import AnsibleModule
import requests

RH_SEC_API = "https://access.redhat.com/hydra/rest/securitydata/cve"

def __get_cve_ids(module_params: dict, module: AnsibleModule) -> map:
  filters = {}
  for filter in ['severity', 'package', 'product']:
    if module_params.get(filter, None):
      filters[filter] = module_params[filter]
  raw = requests.get(f'{RH_SEC_API}.json', params=filters)
  data = raw.json()
  return map(lambda cve: cve['CVE'], data)

def __get_cves_by_severity(ids: str) -> tuple[dict,list]:
  cve_data = {}
  cve_not_found = []
  for cve in ids:
    raw = requests.get(f'{RH_SEC_API}/{cve}.json')
    if raw.status_code != 200:
      cve_not_found.append(cve)
      continue
    data = raw.json()
    severity = data.get('threat_severity', 'unk').lower()
    if severity not in cve_data:
      cve_data[severity] = []
    cve_data[severity].append(data)
  return cve_data, cve_not_found

def main():
  arg_spec = dict(
    ids=dict(
      type="list",
      required=False,
    ),
    severity=dict(
      type="str",
      required=False,
    ),
    package=dict(
      type="str",
      required=False,
    ),
    product=dict(
      type="str",
      required=False,
    ),
    details=dict(
      type="bool",
      required=False,
    ),
  )

  module = AnsibleModule(
    supports_check_mode=True,
    argument_spec=arg_spec,
  )

  if module.params.get('ids', None):
    try:
      cve_data, cve_not_found = __get_cves_by_severity(module.params['ids'])
    except Exception as e:
      module.fail_json(msg=f"Failed to query CVEs by id: {str(e)}")
    module.exit_json(changed=False, cves=cve_data, not_found=cve_not_found)
  else:
    try:
      cve_ids = __get_cve_ids(module.params, module)
      if not module.params.get('details', True):
        module.exit_json(changed=False, cves=list(cve_ids))
      cve_data, cve_not_found = __get_cves_by_severity(cve_ids)
    except Exception as e:
      module.fail_json(msg=f"Failed to query CVEs with filters: {str(e)}")
    module.exit_json(changed=False, cves=cve_data, not_found=cve_not_found)

  ids = module.params.get('ids', None)
  module.exit_json(changed=False, ids=ids)

if __name__ == "__main__":
  main()