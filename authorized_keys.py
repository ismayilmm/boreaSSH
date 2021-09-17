import main
import helper
import connection
from connection import sftp_get
from connection import sftp_put
import host_file_operations as host_op
from dataclasses import dataclass


@dataclass
class AuthorizedKey:
    ssh_definer: str
    ssh_key: str
    ssh_user: str

    def to_string(self):
        return self.ssh_definer + ' ' + self.ssh_key + ' ' + self.ssh_user


def store_authorized_keys_file(file='authorized_keys'):
    authorized_keys = []
    authorized_keys_file = helper.read_lines(file)
    for i, line in enumerate(authorized_keys_file):
        if 'ssh-rsa' in line:
            ssh_definer = line.split(' ')[0]
            ssh_key = line.split(' ')[1]
            ssh_user = line.split(' ')[2]
            authorized_keys.append(AuthorizedKey(ssh_definer, ssh_key, ssh_user))
    return authorized_keys


def get_unique_instances_of_authorized_keys(main_file, auth_file='authorized_keys'):
    auth_keys = store_authorized_keys_file()
    for line in auth_keys:
        if line_in_file(line.ssh_key, main_file) is False:
            main_file.append(AuthorizedKey(line.ssh_definer, line.ssh_key, line.ssh_user))
    return main_file


def line_in_file(ssh_key, main_file):
    check = False
    for line in main_file:
        if line.ssh_key == ssh_key:
            check = True
    return check


def sync_main_file_for_keys(main_auth_keys_file, file='main_file_for_keys'):
    auth_keys = ''
    for key in main_auth_keys_file:
        auth_keys += key.to_string()
    helper.write_to_file(auth_keys, file)


def sync(private_key):
    main_auth_keys_file = store_authorized_keys_file('main_file_for_keys')
    hosts = []
    hosts = host_op.read_file()
    file = ['authorized_keys']
    #for host in hosts:
        #connection.sftp_operation(host.ip, host.username, private_key, file, sftp_get)
        #main_auth_keys_file = get_unique_instances_of_authorized_keys(main_auth_keys_file)

    sync_main_file_for_keys(main_auth_keys_file)
    helper.create_uploadable_file('main_file_for_keys', 'authorized_keys')

