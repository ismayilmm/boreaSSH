from helper_functions import host_file_operations, helper
from dataclasses import dataclass
from helper_functions import connection
from helper_functions.ini_reader import get_full_path
from helper_functions.connection import sftp_get


def sync(private_key):
    main_auth_keys_file = read_authorized_keys_file(get_full_path('main_file_for_keys'))
    hosts = host_file_operations.read_file()
    file = ['authorized_keys']
    for host in hosts:
        connection.sftp_operation(host.ip, host.username, private_key, file, sftp_get)
        main_auth_keys_file = get_unique_instances_of_authorized_keys(main_auth_keys_file)

    sync_main_file_for_keys(main_auth_keys_file)
    helper.create_uploadable_file('main_file_for_keys', 'authorized_keys')


@dataclass
class AuthorizedKey:
    ssh_definer: str
    ssh_key: str
    ssh_user: str

    def to_string(self):
        return self.ssh_definer + ' ' + self.ssh_key + ' ' + self.ssh_user


def read_authorized_keys_file(file=get_full_path('authorized_keys')):
    authorized_keys = []
    for i, line in enumerate(helper.read_lines(file)):
        if 'ssh-rsa' in line:
            ssh_definer = line.split(' ')[0]
            ssh_key = line.split(' ')[1]
            ssh_user = line.split(' ')[2]
            authorized_keys.append(AuthorizedKey(ssh_definer, ssh_key, ssh_user))
    return authorized_keys


def get_unique_instances_of_authorized_keys(main_file, auth_file='authorized_keys'):
    auth_keys = read_authorized_keys_file()
    for line in auth_keys:
        if line_in_file(line.ssh_key, main_file) is False:
            main_file.append(AuthorizedKey(line.ssh_definer, line.ssh_key, line.ssh_user))
    return main_file


def line_in_file(ssh_key, main_file):
    for line in main_file:
        if line.ssh_key == ssh_key:
            return True
    return False


def sync_main_file_for_keys(main_auth_keys_file, file=get_full_path('main_file_for_keys')):
    auth_keys = ''
    for key in main_auth_keys_file:
        auth_keys += key.to_string()
    helper.write_to_file(auth_keys, file)


