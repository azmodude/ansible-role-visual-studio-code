import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_vscode_package(host):
    assert host.package("code").is_installed


def test_vscode_installed(host):
    assert host.file("/usr/bin/code").exists and \
        host.file("/usr/bin/code").is_file


def test_vscode_mayrun(host):
    command = "/usr/bin/code --user-data-dir=/tmp --help"
    assert "Visual Studio Code" in host.command(command).stdout.split("\n")[0]
