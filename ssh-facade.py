import main
import add_new_host
import add_new_customer
import argparse
from dataclasses import dataclass
import getpass


@dataclass
class PrivateKey:
    path: str
    pass_phrase: str


@dataclass
class Input:
    mode: str
    path: str
    pass_phrase: str


parser = argparse.ArgumentParser(description='BoreaSSH')
private_key_path = '/home/' + getpass.getuser() + '/.ssh/id_rsa'
parser.add_argument('--mode', default='sync', help='Working modes: sync, add_host, add_customer')
parser.add_argument('ssh_passphrase', help='SSH passphrase for PK')
args = parser.parse_args()
user_input = Input(args.mode, private_key_path, args.ssh_passphrase)


private_key = PrivateKey(user_input.path, user_input.pass_phrase)
if user_input.mode == 'sync':
    main.sync_it_all_9000(private_key)
elif user_input.mode == 'add_customer':
    add_new_customer.add_customer(private_key)
    print('customer')
elif user_input.mode == 'add_host':
    add_new_host.add_host(private_key)
    print('host')
else:
    print('Expected inputs are: sync, add_host, add_customer')
