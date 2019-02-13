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
    pkg = host.package('docker.io')

    assert pkg.is_installed


def test_package_latest(host):
    changed = host.ansible('package', 'name=docker.io state=latest')['changed']

    assert not changed


def test_program_runs(host):
    host.run_test('docker --version')


def test_service(host):
    svc = host.service('docker')

    assert svc.is_enabled
    assert svc.is_running
