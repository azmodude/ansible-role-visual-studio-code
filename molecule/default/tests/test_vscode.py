import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_vscode_package_isinstalled(host):
    """ Test whether the code package is installed. """
    assert host.package("code").is_installed


def test_vscode_isinpath(host):
    """ Test whether the code command is in PATH. """
    assert host.exists("code")


def test_vscode_mayrun(host):
    """ Test general extension of the code command. """
    command = "code --user-data-dir=/tmp --help"
    assert "Visual Studio Code" in host.command(command).stdout.split("\n")[0]


def test_extension_isinstalled(host):
    """ Test whether requested extensions installed correctly """
    users = host.ansible.get_variables()['vscode_extensions']
    for user in users:
        home = host.user(user['user']).home
        extensions_directory = "{0}/.vscode/extensions".format(home)
        assert host.file(extensions_directory).is_directory

        entries = host.check_output("ls -1 {0}".format(extensions_directory))
        for extension in user['extensions']:
            assert extension in entries
