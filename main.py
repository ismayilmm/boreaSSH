import os
import pysftp


class Hosts:
    def __init__(self, host, hostname, user, port):
        self.host = host
        self.hostname = hostname
        self.user = user
        self.port = port


def open_file(file='storm_list_main'):
    with open(file) as file_lines:
        all_lines = file_lines.readlines()
    return all_lines


def write_to_file(to_write, file='storm_list_main'):
    main_file = open(file, 'a')
    for line in to_write:
        main_file.write(line)
    main_file.close()


def read_hosts_file(file='hosts'):
    return get_host_credentials(open_file(file))


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


def get_storm_list(ip, uname, pwd):
    path_to_file = '/home/' + uname + '/.ssh'
    with pysftp.Connection(host=ip, username=uname, password=pwd) as sftp:
        with sftp.cd(path_to_file):
            sftp.get('config')
    sftp.close()


def store_file(conf_file='config'):
    config = []
    config_file = open_file(conf_file)
    for i in range(0, len(config_file), 4):
        host = config_file[i]
        hostname = config_file[i+1]
        user = config_file[i+2]
        port = config_file[i+3]
        config.append(Hosts(host, hostname, user, port))
    return config


def get_unique_instances(config, main_storm_list):
    for line in config:
        if line_in_file(line.hostname, main_storm_list) is False:
            main_storm_list.append(line)
    return main_storm_list


def line_in_file(auth_key_line, main_file):
    check = False
    for line in main_file:
        if line.hostname == auth_key_line:
            check = True
    return check


def fill_main_storm_list(main_storm_list):
    for line in main_storm_list:
        write_to_file(line.host)
        write_to_file(line.hostname)
        write_to_file(line.user)
        write_to_file(line.port)


def main():
    main_storm_list = store_file(conf_file='storm_list_main')
    hosts = []
    config = []
    hosts = read_hosts_file()
    for host in hosts:
        #get_storm_list(host[0], host[1], host[2])
        config = store_file()
        main_storm_list = get_unique_instances(config, main_storm_list)
    fill_main_storm_list(main_storm_list)


if __name__ == '__main__':
    main()
