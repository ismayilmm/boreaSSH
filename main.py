import os
import pysftp


class Host:
    def __init__(self, host, hostname, user, port):
        self.host = host
        self.hostname = hostname
        self.user = user
        self.port = port

    def to_string(self):
        return self.host + self.hostname + self.user + self.port


def read_lines(file='storm_list_main'):
    with open(file) as file_lines:
        all_lines = file_lines.readlines()
    for line in all_lines:
        if line == '\n ':
            all_lines.remove(line)
    return all_lines


def write_to_file(to_write, file='storm_list_main'):
    main_file = open(file, 'a')
    for line in to_write:
        main_file.write(line)
    main_file.close()


def read_hosts_file(file='hosts'):
    return get_host_credentials(read_lines(file))


def get_host_credentials(host_file):
    hosts = []
    for i, line in enumerate(host_file):
        split_by_space = line.split(' ')

        pwd = format_string(split_by_space[2])
        hosts.append((split_by_space[0], split_by_space[1], pwd))
    return hosts


def format_string(string):
    size = len(string)
    mod_string = string[:size - 1]
    return mod_string


def get_config_file(hostname, username, password):
    private_key_path = "/home/mmd/.ssh/id_rsa"
    path_to_file = '/home/' + username + '/.ssh'
    with pysftp.Connection(hostname, username=username, private_key=private_key_path, private_key_pass='Mmd.123!') as sftp:
        with sftp.cd(path_to_file):
            sftp.get('config')
    sftp.close()


def store_file(conf_file='config'):
    config = []
    config_file = read_lines(conf_file)
    for i in range(0, len(config_file), 4):
        host = config_file[i]
        hostname = config_file[i+1]
        user = config_file[i+2]
        port = config_file[i+3]
        config.append(Host(host, hostname, user, port))
    return config


def get_unique_instances(config, main_storm_list):
    for line in config:
        if hostname_in_file(line.hostname, main_storm_list) is False:
            main_storm_list.append(line)
    return main_storm_list


def hostname_in_file(auth_key_line, main_file):
    for line in main_file:
        if line.hostname == auth_key_line:
            return True
    return False


def sync_main_storm_file(main_storm_list, file='storm_list_main'):
    config = ''
    for host in main_storm_list:
        config += host.to_string()
    write_to_file(config, file)


def main():
    main_storm_list = store_file('storm_list_main')
    hosts, config = [], []
    hosts = read_hosts_file()
    for host in hosts:
        get_config_file(host[0], host[1], host[2])
        config = store_file('config')
        main_storm_list = get_unique_instances(config, main_storm_list)
    sync_main_storm_file(main_storm_list)


if __name__ == '__main__':
    main()
