import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_mount_point(host):
    mnt = host.mount_point('/mnt/add_disk')

    assert mnt.exists
    assert mnt.filesystem == 'ext4'
    assert mnt.device == '/dev/loop0p1'
