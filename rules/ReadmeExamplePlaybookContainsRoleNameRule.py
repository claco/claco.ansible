from ansiblelint import AnsibleLintRule
import os
import re


class ReadmeExamplePlaybookContainsRoleNameRule(AnsibleLintRule):
    id = '1011'
    shortdesc = 'README Example Playbook must contain the role name'
    info = 'author'
    description = (
        'All README files Example Playbook section must contain the role name'
    )
    severity = 'MEDIUM'
    tags = ['role', 'style', 'formatting']
    version_added = 'v4.0.0'

    def matchplay(self, file, data):
        if file['type'] != 'meta':
            return False

        path_parts = file['path'].split(os.path.sep)

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
        path_parts.append('README.md')
        readme = os.path.sep.join(path_parts)

        results = []

        with open(readme) as f:
            lines = f.readlines()
            examples = []

            for i in range(0, len(lines)):
                line = lines[i].strip()
                if line == 'Example Playbook':
                    examples = lines[i+1:]
                    break

            if re.search('         .* role: %s' % role_name, ''.join(examples)):
                return False
            else:
                results.append(({'README.md': data},
                               'README Example Playbook must contain the role name "%s"' % role_name))

        return results
