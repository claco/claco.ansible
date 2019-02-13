from ansiblelint import AnsibleLintRule
import glob
import os
import re


class VariablesInAlphabeticalOrderRule(AnsibleLintRule):
    id = '1012'
    shortdesc = 'Role defaults and variables must be in alphabetical order'
    info = 'author'
    description = (
        'All variables in role defaults and variables files must be in alphabetical order'
    )
    severity = 'MEDIUM'
    tags = ['role', 'style', 'formatting']
    version_added = 'v4.0.0'

    def matchplay(self, file, data):
        if file['type'] != 'meta':
            return False

        path_parts = file['path'].split(os.path.sep)
        path_parts = [part for part in path_parts if part]

        role_name = path_parts.pop()
        part = path_parts.pop()

        while path_parts:
            if part == 'roles':
                break
            else:
                role_name = path_parts.pop()
                part = path_parts.pop()

        path_parts.append(part)
        path_parts.append(role_name)

        defaults_path_parts = list(path_parts)
        defaults_path_parts.append('defaults')
        defaults_path_parts.append('*.yml')
        defaults_files = glob.glob(os.path.sep.join(defaults_path_parts))
        defaults_files.sort()

        vars_path_parts = list(path_parts)
        vars_path_parts.append('vars')
        vars_path_parts.append('*.yml')
        vars_files = glob.glob(os.path.sep.join(vars_path_parts))
        vars_files.sort()

        r = re.compile('^(?!#|---| |\n)')

        results = []

        for file in (defaults_files + vars_files):
            with open(file) as f:
                contents = list(filter(r.match, f.readlines()))
                sorted_contents = list(contents)
                sorted_contents.sort()

                if contents != sorted_contents:
                    file_path = file.replace(os.path.sep.join(path_parts) + os.path.sep, '')
                    results.append(({file: data},
                                   'Variables must be in alphabetical order %s: "%s"' % (role_name, file_path)))

        return results
