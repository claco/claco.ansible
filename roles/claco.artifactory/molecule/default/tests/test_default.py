import os
import requests
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_artifactory_service(host):
    svc = host.docker('artifactory')

    assert svc.is_running


def test_artifactory_socket(host):
    socket = host.socket('tcp://0.0.0.0:8081')

    assert socket.is_listening


def test_artifactory_responds(host):
    response = requests.get('http://localhost:8081/')

    assert response.status_code == 200


@pytest.mark.parametrize('name', [
  ('claco-ansible-development-local'),
  ('claco-ansible-staging-local'),
  ('claco-ansible-production-local')
])
def test_artifactory_repositories(host, name):
    response = requests.get('http://localhost:8081/artifactory/%s/' % name)

    assert response.status_code == 200
