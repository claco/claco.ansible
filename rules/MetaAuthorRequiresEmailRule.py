from ansiblelint import AnsibleLintRule
import re


class MetaAuthorRequiresEmailRule(AnsibleLintRule):
    id = '1002'
    shortdesc = 'meta/main.yml author must contain an email address'
    info = 'author'
    description = (
        'meta/main.yml author must contain an email address after the name: First Last <email@example.com>'
    )
    severity = 'HIGH'
    tags = ['metadata']
    version_added = 'v4.0.0'

    def matchplay(self, file, data):
        if file['type'] != 'meta':
            return False

        galaxy_info = data.get('galaxy_info', None)
        if not galaxy_info:
            return [({'meta/main.yml': data},
                    "No 'galaxy_info' found")]

        results = []
        if not galaxy_info.get(self.info, None):
            results.append(({'meta/main.yml': data},
                            'Role info should contain %s' % self.info))

        author = galaxy_info.get(self.info, None)
        if not author:
            return [({'meta/main.yml': data},
                     'Author information is missing from main/meta.yml')]

        if not re.search('<.*@.*>', author):
            results.append(({'meta/main.yml': data},
                            'Author "%s" must contain an email address after the name: ' % author +
                            'First Last <email@example.com>'))

        return results
