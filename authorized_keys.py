import main
import helper


def get_unique_instances_of_authorized_keys(main_file, auth_file='authorized_keys'):
    auth_keys = helper.read_lines(auth_file)
    for line in auth_keys:
        if line_in_file(line, main_file) is False:
            main_file.append(line)
    return main_file


def line_in_file(auth_key_line, main_file):
    check = False
    ssh_key = auth_key_line.split(' ')[1]
    for line in main_file:
        if line.split(' ')[1] == ssh_key:
            check = True
    return check


def sync_main_file_for_keys(main_auth_keys_file):
    helper.write_to_file(main_auth_keys_file, 'main_file_for_keys')


def sync(private_key):
    main_auth_keys_file = helper.read_lines('main_file_for_keys')
    hosts = []
    hosts = helper.read_hosts_file()
    for host in hosts:
        helper.get_file(host[0], host[1], private_key[0], private_key[1], 'authorized_keys')
        main_auth_keys_file = get_unique_instances_of_authorized_keys(main_auth_keys_file)

    sync_main_file_for_keys(main_auth_keys_file)
    helper.create_uploadable_file('main_file_for_keys', 'authorized_keys')

