from main_functions import add_new_host, add_new_customer, authorized_keys, storm
from helper_functions import helper
import argparse
from dataclasses import dataclass
import getpass
import logging
from helper_functions.ini_reader import get_log_path as path

logging.basicConfig(filename=path('boreaSSH.log'), filemode='a', format='%(name)s - %(levelname)s - %(message)s')


def sync_operation():
    logging.info('Syncing authorized_keys file...')
    authorized_keys.sync(private_key)
    logging.info('Syncing config file...')
    storm.sync(private_key)
    logging.info('Syncing updated files with hosts...')
    helper.sync_files_with_hosts(private_key)


@dataclass
class PrivateKey:
    path: str
    pass_phrase: str


@dataclass
class Input:
    mode: str
    path: str
    pass_phrase: str


# parser = argparse.ArgumentParser(description='BoreaSSH')
# private_key_path = '/home/' + getpass.getuser() + '/.ssh/id_rsa'
# parser.add_argument('--mode', default='sync', help='Working modes: sync, add_host, add_customer')
# parser.add_argument('ssh_passphrase', help='SSH passphrase for PK')
# args = parser.parse_args()
# user_input = Input(args.mode, private_key_path, args.ssh_passphrase)
# private_key = PrivateKey(user_input.path, user_input.pass_phrase)


user_input = Input('sync', '/Users/ismayilmammadli/.ssh/id_rsa', 'asdasd')
private_key = PrivateKey('/Users/ismayilmammadli/.ssh/id_rsa', 'asdasd')


if user_input.mode == 'sync':
    sync_operation()
elif user_input.mode == 'add_customer':
    logging.info('Adding a new customer')
    add_new_customer.add_customer(private_key)
    sync_operation()
elif user_input.mode == 'add_host':
    logging.info('Adding new host')
    add_new_host.add_host(private_key)
    sync_operation()
else:
    logging.warning('Expected inputs are: sync, add_host, add_customer')
    print('Expected inputs are: sync, add_host, add_customer')
