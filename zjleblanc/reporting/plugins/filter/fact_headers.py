#!/usr/bin/python
class FilterModule(object):
    def filters(self):
        return {
            'fact_headers': self.do_get_fact_headers
        }

    def do_get_fact_headers(self, data_model, config):
      has_limit = len(config.get('limit'))
      has_limit_prefix = len(config.get('limit_prefix'))
      has_exclude = len(config.get('exclude'))
      has_exclude_prefix = len(config.get('exclude_prefix'))
      
      filtered = []
      for key in data_model.keys():
        # always first column
        if key == 'inventory_hostname':
          continue
        # dicts / lists are not only visible in json tree
        if isinstance(data_model[key], dict) or isinstance(data_model[key], list):
          continue
        # process limits
        if has_limit and key in config.get('limit'):
          filtered.append(key)
          continue
        if has_limit_prefix and key.startswith(config.get('limit_prefix')):
          filtered.append(key)
          continue
        # process exclusions
        if has_exclude and key in config.get('exclude'):
          continue
        if has_exclude_prefix and key.startswith(config.get('exclude_prefix')):
          continue
        # no limits and not excluded
        if not has_limit and not has_limit_prefix:
          filtered.append(key)

      return filtered