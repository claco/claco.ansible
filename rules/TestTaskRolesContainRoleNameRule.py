from ansiblelint import AnsibleLintRule
import os


class TestTaskRolesContainRoleNameRule(AnsibleLintRule):
    id = '1008'
    shortdesc = 'Role test playbooks roles must include the current role: "- role: role_name"'
    info = 'author'
    description = (
        'All role test playbooks roles must include the current role: "-role: role_name"'
    )
    severity = 'MEDIUM'
    tags = ['tests', 'roles']
    version_added = 'v4.0.0'

    def matchplay(self, file, data):
        if file['type'] != 'playbook':
            return False

        path = file.get('path', None)
        path_parts = path.split(os.path.sep)
        path_parts = [part for part in path_parts if part]

        if not (path_parts.pop() == 'test.yml' and path_parts.pop() == 'tests'):
            return False

        part = path_parts.pop(0)
        role_name = None

        while path_parts:
            if part == 'roles':
                role_name = path_parts.pop(0)

                break
            else:
                break

        results = []

        if role_name and role_name not in data['roles']:
            results.append(({'tests/test.yml': data}, 'Role tests playbook roles must include ' +
                            'the current role %s: "%s"' % (role_name, ','.join(data['roles']))))

        return results
