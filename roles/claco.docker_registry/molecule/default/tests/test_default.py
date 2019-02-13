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


def test_docker_registry_service(host):
    svc = host.docker('docker-registry')

    assert svc.is_running


def test_docker_registry_socket(host):
    socket = host.socket('tcp://0.0.0.0:5000')

    assert socket.is_listening


def test_docker_registry_responds(host):
    response = requests.get('http://localhost:5000/')

    assert response.status_code == 200
