#!/usr/bin/python
import re

class FilterModule(object):
  def filters(self):
    return {
      'parse_updates': self.do_parse_updates
    }

  # Expected format: https://docs.oracle.com/en/database/oracle/oracle-database/19/ladbi/rpm-packages-naming-convention.html
  def do_parse_updates(self, pkg_output):
    installed = {}
    updated = {}
    removed = {}

    for result in filter(lambda res: res.lower().startswith('installed'), pkg_output):
      name, meta = self.__parse_result(result.split(' ')[-1])
      installed[name.lower()] = meta

    for result in filter(lambda res: res.lower().startswith('removed'), pkg_output):
      name, meta = self.__parse_result(result.split(' ')[-1])

      name = name.lower()
      pkg = installed.pop(name, None)
      if pkg:
        pkg['old_version'] = meta['version']
        updated[name] = pkg
      else:
        removed[name] = meta

    return {
      "installed": installed,
      "updated": updated,
      "removed": removed
    }
      

  def __parse_result(self, res) -> tuple[str, dict]:
    if ':' in res:
      return self.__parse_with_colon(res)
    if 'git' in res:
      return self.__parse_with_git(res)
    
    return self.__parse_std(res)

  def __parse_with_colon(self, res) -> tuple[str, dict]:
    tokens = res.split(':')
    name = tokens[0]

    tokens = ':'.join(tokens[1:]).split('.')
    arch = tokens[-1]
    release = tokens[-2]
    version = '.'.join(tokens[0:-2])

    return name, {"arch": arch, "release": release, "version": version}


  def __parse_with_git(self, res) -> tuple[str, dict]:
    tokens = res.split('.')
    arch = tokens[-1]
    release = tokens[-2]
    version = tokens[-3]

    namever = '.'.join(tokens[0:-3])
    match = re.search(r"-\d", namever)
    if match:
      version = namever[match.start()+1:] + '.' + version
      name = namever[:match.start()]
    else:
      name = namever

    return name, {"arch": arch, "release": release, "version": version}

  def __parse_std(self, res) -> tuple[str, dict]:
    tokens = res.split('.')
    arch = tokens[-1]
    release = tokens[-2]

    namever = '.'.join(tokens[0:-2])
    match = re.search(r"-\d", namever)
    if match:
      version = namever[match.start()+1:]
      name = namever[:match.start()]
    else:
      name = namever
      raise Exception(f"parse_std: Failed to parse output -> {res}")

    return name, {"arch": arch, "release": release, "version": version}