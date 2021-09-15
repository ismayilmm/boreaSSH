import argparse
import authorized_keys
import storm
import helper


def private_key_credentials():
    parser = argparse.ArgumentParser()
    parser.add_argument("private_key_path", type=str)
    parser.add_argument("private_key_pass", type=str)
    args = parser.parse_args()
    print('Args: ' + str(args))
    private_key_path = args.private_key_path
    private_key_pass = args.private_key_pass
    print(private_key_path)
    print(private_key_pass)
    return private_key_path, private_key_pass


def main():
    #private_key = private_key_credentials()
    private_key = ['/home/mmd/.ssh/id_rsa', 'Mmd.123!']
    authorized_keys.sync(private_key)
    storm.sync(private_key)
    helper.sync_files_with_hosts(private_key[0], private_key[1])


if __name__ == '__main__':
    main()
