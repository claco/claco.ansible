from ansiblelint import AnsibleLintRule
import re
import os


class DefaultHeaderCommentMatchesRoleNameRule(AnsibleLintRule):
    id = '1003'
    shortdesc = 'Role header comments must match role name: "# defaults file for role.name"'
    info = 'author'
    description = (
        'All role files with comment headers must match the name of the role containing them: ' +
        '"# defaults file for role.name"'
    )
    severity = 'MEDIUM'
    tags = ['role', 'style', 'formatting']
    version_added = 'v4.0.0'

    def match(self, file, text):
        if text != '---':
            return False

        # ansible-lint helpfully strips comments from the input :-/
        with open(file['path']) as f:
            # toss the yaml header
            f.readline()

            # read what should be a comment line
            comment = f.readline().strip()

            # check that the line is a comment
            if not re.search('^# ', comment):
                return 'Second line is not a comment: "%s"' % comment

            # check that the comment has the matching role name
            path_parts = f.name.split(os.path.sep)
            path_parts = [part for part in path_parts if part]
            part = path_parts.pop(0)

            while path_parts:
                if part == 'roles':
                    name = path_parts.pop(0)
                    if not re.search('( file for %s$| playbook to )' % name, comment):
                        return 'Role header does not contain role name: "%s"' % name
                    break
                else:
                    part = path_parts.pop(0)

            # check that the next line is EOF or blank
            next_line = f.readline().strip()
            if next_line and next_line != '':
                return 'Line after Role comment header must be blank or EOF: "%s"' % next_line

        return False
