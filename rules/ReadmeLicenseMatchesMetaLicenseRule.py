from ansiblelint import AnsibleLintRule
import os


class ReadmeLicenseMatchesMetaLicenseRule(AnsibleLintRule):
    id = '1006'
    shortdesc = 'README License must match meta file license value'
    info = 'author'
    description = (
        'All README files License section must match the license value declared in the roles meta file'
    )
    severity = 'MEDIUM'
    tags = ['role', 'style', 'formatting']
    version_added = 'v4.0.0'

    def matchplay(self, file, data):
        if file['type'] != 'meta':
            return False

        license = data['galaxy_info']['license']

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
                if line == 'License':
                    value = lines[i+3].strip()

                    if value != license:
                        results.append(({'README.md': data},
                                        'README License must be the same as the meta file license %s: "%s"' %
                                        (license, value)))

                    break

        return results
