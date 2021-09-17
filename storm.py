import main
import helper
import connection
import host_file_operations as host_op


class StormHost:
    def __init__(self, host, hostname, user, port):
        self.host = host
        self.hostname = hostname
        self.user = user
        self.port = port

    def to_string(self):
        return self.host + self.hostname + self.user + self.port


def add_new_host(host, hostname, user, port):
    host = 'Host ' + host + '\n'
    hostname = '   hostname ' + hostname + '\n'
    user = '   user ' + user + '\n'
    port = '   port ' + port
    new_host = host + hostname + user + port
    helper.append_to_file(new_host, 'storm_list_main')


def store_config_file(conf_file='config'):
    config = []
    host, hostname, user, port = '', '', '', ''
    config_file = helper.read_lines(conf_file)
    for i, line in enumerate(config_file):
        if 'Host' in line:
            host = line
        elif 'hostname' in line:
            hostname = line
        elif 'user' in line:
            user = line
        elif 'port' in line:
            port = line
            config.append(StormHost(host, hostname, user, port))
    return config


def get_unique_instances_of_config_file(config, main_storm_list):
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
    helper.write_to_file(config, file)


def sync(private_key):
    main_storm_list = store_config_file('storm_list_main')
    hosts, config = [], []
    hosts = host_op.read_file()
    file = ['config']
    for host in hosts:
        connection.sftp_operation(host.ip, host.username, private_key, file, connection.sftp_get)
        config = store_config_file('config')
        config.reverse()
        main_storm_list = get_unique_instances_of_config_file(config, main_storm_list)
    sync_main_storm_file(main_storm_list)
    helper.create_uploadable_file('storm_list_main', 'config')
