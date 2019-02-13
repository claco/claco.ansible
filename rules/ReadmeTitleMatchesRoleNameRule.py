from ansiblelint import AnsibleLintRule
import os


class ReadmeTitleMatchesRoleNameRule(AnsibleLintRule):
    id = '1005'
    shortdesc = 'README title must match role name: "role.name\n========="'
    info = 'author'
    description = (
        'All README files titles must match the name of the role containing them: ' +
        '"role.name\n========="'
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
            title = f.readline().strip()
            if title != role_name:
                results.append(({'README.md': data},
                               'README title must match role name %s: "%s"' % (role_name, title)))

            title_size = f.readline().strip()
            title_header = ("=" * len(role_name))
            if title_size != title_header:
                results.append(({'README.md': data},
                               'Line after README role name must be markdown header size "%s": "%s"' %
                                (title_header, title_size)))

        return results
