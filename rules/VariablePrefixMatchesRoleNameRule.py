from ansiblelint import AnsibleLintRule
import re
import os


class VariablePrefixMatchesRoleNameRule(AnsibleLintRule):
    id = '1004'
    shortdesc = 'Role defaults and variables must be prefixed with the role name: "role_name_variable:"'
    info = 'author'
    description = (
        'All role defaults and variables files variables names must be prefixed with the name of the role ' +
        'containing them: "role_name_variable:"'
    )
    severity = 'HIGH'
    tags = ['defaults', 'variables', 'style']
    version_added = 'v4.0.0'

    def match(self, file, text):
        path = file.get('path', None)
        type = file.get('type', None)

        if type != 'playbook':
            return False

        if text in ('---', '', None):
            return False

        if re.search('^#? ', text):
            return False

        path_parts = path.split(os.path.sep)
        path_parts = [part for part in path_parts if part]

        part = path_parts.pop(0)
        role_name = None
        variable_prefix = None
        actual_variable = None
        file_type = None

        while path_parts:
            if part == 'roles':
                role_name = path_parts.pop(0)
                variable_prefix = role_name.split('.').pop() + '_'
                file_type = path_parts.pop(0)
                actual_variable = text.split(':').pop(0)

                break
            else:
                break

        if role_name and file_type:
            if file_type in ('defaults', 'vars'):
                if not re.search('^%s' % variable_prefix, text):
                    return 'Role defaults and variables must be prefixed with the role name %s: "%s"' \
                           % (variable_prefix, actual_variable)

        return False
