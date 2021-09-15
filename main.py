import os
import pysftp
import shutil
import argparse


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


class Host:
    def __init__(self, host, hostname, user, port):
        self.host = host
        self.hostname = hostname
        self.user = user
        self.port = port

    def to_string(self):
        return self.host + self.hostname + self.user + self.port


def store_file(conf_file='config'):
    config = []
    config_file = read_lines(conf_file)
    for i, line in enumerate(config_file):
        if 'Host' in line:
            host = line
        elif 'hostname' in line:
            hostname = line
        elif 'user' in line:
            user = line
        elif 'port' in line:
            port = line
            config.append(Host(host, hostname, user, port))
    return config


def read_hosts_file(file='hosts'):
    return get_host_credentials(read_lines(file))


def get_host_credentials(host_file):
    hosts = []
    for i, line in enumerate(host_file):
        split_by_space = line.split(' ')
        uname = format_string(split_by_space[1])
        hosts.append((split_by_space[0], uname))
    return hosts


def format_string(string):
    size = len(string)
    mod_string = string[:size - 1]
    return mod_string


def read_lines(file='storm_list_main'):
    with open(file) as file_lines:
        all_lines = file_lines.readlines()
    for line in all_lines:
        if line == '\n ':
            all_lines.remove(line)
    return all_lines


def write_to_file(to_write, file='storm_list_main'):
    main_file = open(file, 'w')
    for line in to_write:
        main_file.write(line)
    main_file.close()


def get_config_file(hostname, username, private_key_path, private_key_pass):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    path_to_file = '/home/' + username + '/.ssh'
    port_no = 22
    if username == 'ural':
        port_no = 9669
    with pysftp.Connection(hostname, username=username, private_key=private_key_path, private_key_pass=private_key_pass, port=port_no, cnopts=cnopts) as sftp:
        with sftp.cd(path_to_file):
            sftp.get('config')
    sftp.close()


def get_unique_instances(config, main_storm_list):
    for line in config:
        if hostname_in_file(line.hostname, line.port, main_storm_list) is False:
            main_storm_list.append(line)
    return main_storm_list


def hostname_in_file(auth_key_host, auth_key_port, main_file):
    for line in main_file:
        if line.hostname == auth_key_host and line.port == auth_key_port:
            return True
    return False


def sync_main_storm_file(main_storm_list, file='storm_list_main'):
    config = ''
    for host in main_storm_list:
        config += host.to_string()
    write_to_file(config, file)


def create_uploadable_file(old_name='storm_list_main', new_name='config'):
    current_directory = os.getcwd()
    shutil.copy(old_name, current_directory + "/" + new_name)


def upload_config_file(ip, uname, private_key_path, private_key_pass):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    path_to_file = '/home/' + uname + '/.ssh'
    port_no = 22
    if uname == 'ural':
        port_no = 9669
    with pysftp.Connection(host=ip, username=uname, private_key=private_key_path, private_key_pass=private_key_pass, port=port_no, cnopts=cnopts) as sftp:
        with sftp.cd(path_to_file):
            sftp.put('config')
    sftp.close()


def sync_config_with_hosts(hosts, private_key_path, private_key_pass):
    for host in hosts:
        upload_config_file(host[0], host[1], private_key_path, private_key_pass)


def main():
    #private_key = private_key_credentials()
    private_key = []
    private_key[0] = '/home/mmd/.ssh/id_rsa'
    private_key[1] = 'Mmd.123!'
    main_storm_list = store_file('storm_list_main')
    hosts, config = [], []
    hosts = read_hosts_file()
    for host in hosts:
        get_config_file(host[0], host[1], private_key[0], private_key[1])
        config = store_file('config')
        config.reverse()
        main_storm_list = get_unique_instances(config, main_storm_list)
    sync_main_storm_file(main_storm_list)
    create_uploadable_file()
    #sync_config_with_hosts(hosts, private_key[0], private_key[1])


if __name__ == '__main__':
    main()

