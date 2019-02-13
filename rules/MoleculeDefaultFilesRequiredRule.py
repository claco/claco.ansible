from ansiblelint import AnsibleLintRule
import os


class MoleculeDefaultFilesRequiredRule(AnsibleLintRule):
    id = '1009'
    shortdesc = 'Roles require the Molecule default testing scenario files'
    info = 'author'
    description = (
        'All roles require the Molecule default testing scnenario files'
    )
    severity = 'MEDIUM'
    tags = ['role', 'style', 'testing']
    version_added = 'v4.0.0'
    files = ['cleanup.yml', 'Dockerfile.j2', 'INSTALL.rst', 'molecule.yml', 'playbook.yml',
             'prepare.yml', 'requirements.yml', 'side_effect.yml', 'tests/test_default.py']

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
        path_parts.append('molecule')
        path_parts.append('default')

        results = []

        for file in self.files:
            path = os.path.sep.join(path_parts + [file])

            if not os.path.isfile(path):
                results.append(({path: data},
                               'Molecule file does not exist: molecule/default/%s' % file))

        return results
