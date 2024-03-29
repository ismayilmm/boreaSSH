#!/usr/bin/env python

from main_functions import authorized_keys
from dataclasses import dataclass
from helper_functions import host_file_operations, helper, connection
from main_functions import storm
import getpass


@dataclass
class NewHost:
    ip: str
    username: str
    password: str
    alias: str
    port: str


def get_new_user_credentials():
    ip = input('Please enter ip of the new host: ')
    username = input('Please enter username of the new host: ')
    password = getpass.getpass('Please enter password of the new host: ')
    alias = input('Please enter alias of the new host: ')
    port = input('Please enter the port number of the new host: ')
    return NewHost(ip, username, password, alias, port)


def add_host(private_key):
    #private_key = ('/home/mmd/.ssh/id_rsa', 'Mmd.123!')
    authorized_keys.sync(private_key)
    storm.sync(private_key)
    helper.sync_files_with_hosts(private_key)
    new_user = get_new_user_credentials()
    connection.sftp_password_operation(new_user.ip, new_user.username, new_user.password)
    storm.add_new_host(new_user.alias, new_user.ip, new_user.username, new_user.port)
    host_file_operations.add_new_host(new_user.ip, new_user.username)
    authorized_keys.sync(private_key)
    storm.sync(private_key)
    helper.sync_files_with_hosts(private_key)


if __name__ == '__main__':
    add_host()
