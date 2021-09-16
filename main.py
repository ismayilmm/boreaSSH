import argparse
import authorized_keys
import storm
import helper
from dataclasses import dataclass


@dataclass
class PrivateKey:
    path: str
    pass_phrase: str


def private_key_credentials():
    parser = argparse.ArgumentParser()
    parser.add_argument("private_key_path", type=str)
    parser.add_argument("private_key_pass", type=str)
    args = parser.parse_args()
    private_key = PrivateKey(args.private_key_path, args.private_key_pass)
    return private_key


def sync_it_all_9000():
    #private_key = private_key_credentials()
    private_key = PrivateKey('/home/mmd/.ssh/id_rsa', 'Mmd.123!')
    authorized_keys.sync(private_key)
    storm.sync(private_key)
    helper.sync_files_with_hosts(private_key)


if __name__ == '__main__':
    sync_it_all_9000()


"""
3. authorized keys dataclass
"""