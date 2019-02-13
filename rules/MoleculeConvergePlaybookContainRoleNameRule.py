from ansiblelint import AnsibleLintRule
import os


class MoleculeConvergePlaybookContainRoleNameRule(AnsibleLintRule):
    id = '1010'
    shortdesc = 'Roles Molecule converge playbook must include the current role: "- role: role_name"'
    info = 'author'
    description = (
        'All roles Molecule converge playbook must include the current role: "-role: role_name"'
    )
    severity = 'MEDIUM'
    tags = ['tests', 'roles', 'molecule']
    version_added = 'v4.0.0'

    def matchplay(self, file, data):
        if file['type'] != 'playbook':
            return False

        path = file.get('path', None)
        path_parts = path.split(os.path.sep)
        path_parts = [part for part in path_parts if part]

        playbook = path_parts.pop()
        scenario = path_parts.pop()

        if not (playbook == 'playbook.yml' and scenario in ['default'] and path_parts.pop() == 'molecule'):
            return False

        if not path_parts:
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
        roles = [role['role'] for role in data['roles']]

        if role_name and role_name not in roles:
            error_file_path = 'molecule/%s/playbook.yml' % scenario

            results.append(({error_file_path: data}, 'Roles Molecule converge playbook must include ' +
                            'the current role %s: "%s"' % (role_name, ','.join(roles))))

        return results
