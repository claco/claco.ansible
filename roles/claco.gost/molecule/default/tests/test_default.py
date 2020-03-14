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
    pkg = host.find_command('gost', extrapaths=['/root/go/bin'])

    assert pkg


def test_program_runs(host):
    host.run_test('/root/go/bin/gost help')
