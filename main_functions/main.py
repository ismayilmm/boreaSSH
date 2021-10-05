#!/usr/bin/env python
import argparse
from main_functions import authorized_keys, storm
from helper_functions import helper
from dataclasses import dataclass
import getpass


@dataclass
class PrivateKey:
    path: str
    pass_phrase: str


def private_key_credentials():
    parser = argparse.ArgumentParser()
    private_key_path = '/home/' + getpass.getuser() + '/.ssh/id_rsa'
    parser.add_argument("private_key_pass", type=str)
    args = parser.parse_args()
    return PrivateKey(private_key_path, args.private_key_pass)


def sync_it_all_9000(private_key):
    #private_key = private_key_credentials()
    #private_key = PrivateKey('/home/mmd/.ssh/id_rsa', 'Mmd.123!')
    authorized_keys.sync(private_key)
    storm.sync(private_key)
    helper.sync_files_with_hosts(private_key)


if __name__ == '__main__':
    sync_it_all_9000()
