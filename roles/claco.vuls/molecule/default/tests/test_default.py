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
    pkg = host.find_command('vuls', extrapaths=['/root/go/bin'])

    assert pkg


def test_program_runs(host):
    host.run_test('/root/go/bin/vuls help')


def test_config_exists(host):
    assert host.file('/opt/vuls/config.toml').exists


def test_cve_db_exists(host):
    assert host.file('/opt/vuls/cve.sqlite3').exists


def test_gost_db_exists(host):
    assert host.file('/opt/vuls/gost.sqlite3').exists


def test_oval_db_exists(host):
    assert host.file('/opt/vuls/oval.sqlite3').exists
