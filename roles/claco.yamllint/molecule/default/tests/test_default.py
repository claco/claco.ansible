import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_package_installed(host):
    pkgs = host.pip_package.get_packages(pip_path='~/.venv/bin/pip')

    assert pkgs.get('yamllint', None)


def test_package_latest(host):
    changed = host.ansible('pip', 'name=yamllint state=latest', check=False)['changed']

    assert not changed


def test_program_runs(host):
    host.run_test('~/.venv/bin/yamllint --version')
