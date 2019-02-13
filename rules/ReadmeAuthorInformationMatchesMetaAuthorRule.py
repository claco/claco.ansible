from ansiblelint import AnsibleLintRule
import os


class ReadmeAuthorInformationMatchesMetaAuthorRule(AnsibleLintRule):
    id = '1007'
    shortdesc = 'README Author Information must match meta file author value'
    info = 'author'
    description = (
        'All README files Author Information section must match the author value declared in the roles meta file'
    )
    severity = 'MEDIUM'
    tags = ['role', 'style', 'formatting']
    version_added = 'v4.0.0'

    def matchplay(self, file, data):
        if file['type'] != 'meta':
            return False

        author = data['galaxy_info'].get('author', None)
        if not author:
            return [({'README.md': data},
                     'Author information is missing from main/meta.yml')]

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

            for i in range(0, len(lines)):
                line = lines[i].strip()
                if line == 'Author Information':
                    value = lines[i+3].strip()

                    if value != author:
                        results.append(({'README.md': data},
                                        'README Author Information must be the same as the meta file author %s: "%s"' %
                                        (author, value)))

                    break

        return results
