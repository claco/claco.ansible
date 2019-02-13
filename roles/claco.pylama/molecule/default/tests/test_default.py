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

    assert pkgs.get('pylama', None)


def test_package_latest(host):
    pylama_changed = host.ansible('pip', 'name=pylama state=latest', check=False)['changed']
    eradicate_changed = host.ansible('pip', 'name=eradicate state=latest', check=False)['changed']

    assert not pylama_changed
    assert not eradicate_changed


def test_program_runs(host):
    host.run_test('~/.venv/bin/pylama --version')
    host.run_test('~/.venv/bin/eradicate --version')
