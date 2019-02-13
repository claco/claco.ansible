import os
import requests

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_teamcity_server_service(host):
    svc = host.docker('teamcity-server')

    assert svc.is_running


def test_teamcity_server_socket(host):
    socket = host.socket('tcp://0.0.0.0:8111')

    assert socket.is_listening


def test_teamcity_server_responds(host):
    response = requests.get('http://localhost:8111/')

    assert response.status_code == 401
    assert 'Authentication required' in response.text
