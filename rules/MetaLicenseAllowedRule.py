from ansiblelint import AnsibleLintRule


class MetaLicenseAllowedRule(AnsibleLintRule):
    id = '1001'
    shortdesc = 'meta/main.yml license must be an approved license'
    info = 'license'
    licenses = ['MIT']
    description = (
        'meta/main.yml license must be one of the approved licenses: ``{}``'.format(', '.join(licenses))
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

        license = galaxy_info.get(self.info, None)
        if license not in self.licenses:
            results.append(({'meta/main.yml': data},
                            'License "%s" must be one of the approved licenses %s:' % (license, self.licenses)))

        return results
