import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_teamcity_build_agent_service(host):
    svc = host.docker('teamcity-build-agent-1')

    assert svc.is_running


def test_teamcity_build_agent_socket(host):
    socket = host.socket('tcp://0.0.0.0:9090')

    assert socket.is_listening
