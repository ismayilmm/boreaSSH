#!/usr/bin/env python


from main_functions import authorized_keys
from helper_functions import helper, connection
from dataclasses import dataclass
from main_functions import storm
import getpass


@dataclass
class NewCustomer:
    ip: str
    username: str
    password: str
    alias: str
    port: str


def get_new_user_credentials():
    ip = input('Please enter ip of the new customer: ')
    username = input('Please enter username of the new customer: ')
    password = getpass.getpass('Please enter password of the new customer: ')
    alias = input('Please enter alias of the new customer: ')
    port = input('Please enter the port number of the new customer: ')
    return NewCustomer(ip, username, password, alias, port)


def add_customer(private_key):
    #private_key = ('/home/mmd/.ssh/id_rsa', 'Mmd.123!')
    #private_key = main.private_key_credentials()
    authorized_keys.sync(private_key)
    storm.sync(private_key)
    helper.sync_files_with_hosts(private_key)
    new_user = get_new_user_credentials()
    connection.sftp_password_operation(new_user.ip, new_user.username, new_user.password)
    storm.add_new_host(new_user.alias, new_user.ip, new_user.username, new_user.port)
    authorized_keys.sync(private_key)
    storm.sync(private_key)
    helper.sync_files_with_hosts(private_key)
