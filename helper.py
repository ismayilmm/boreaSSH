import main
import storm
import authorized_keys
import os
import pysftp
import shutil


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
    mod_string = string
    if '\n' in string:
        size = len(string)
        mod_string = string[:size - 1]
    return mod_string


def read_lines(file='storm_list_main'):
    with open(file) as file_lines:
        all_lines = file_lines.readlines()
    for line in all_lines:
        if line == '\n':
            all_lines.remove(line)
    return all_lines


def write_to_file(to_write, file='storm_list_main'):
    main_file = open(file, 'w')
    for line in to_write:
        main_file.write(line)
    main_file.close()


def port_no(username):
    return 9669 if username == 'ural' else 22


def get_file(hostname, username, private_key_path, private_key_pass, file):
    with pysftp.Connection(hostname, username=username, private_key=private_key_path, private_key_pass=private_key_pass,
                           port=port_no(username), cnopts=connection_options()) as sftp:
        with sftp.cd('/home/' + username + '/.ssh'):
            sftp.get(file)
    sftp.close()


def create_uploadable_file(old_name='storm_list_main', new_name='config'):
    current_directory = os.getcwd()
    shutil.copy(old_name, current_directory + "/" + new_name)


def connection_options():
    """
    Note
    """
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    return cnopts


def upload_files(ip, uname, private_key_path, private_key_pass, files):
    with pysftp.Connection(host=ip, username=uname, private_key=private_key_path, private_key_pass=private_key_pass,
                           port=port_no(uname), cnopts=connection_options()) as sftp:
        with sftp.cd('/home/' + uname + '/.ssh'):
            for file in files:
                sftp.put(file)
    sftp.close()


def sync_files_with_hosts(private_key_path, private_key_pass):
    hosts = read_hosts_file()
    files = ['authorized_keys', 'config']
    for host in hosts:
        upload_files(host[0], host[1], private_key_path, private_key_pass, files)
    #sftp_operation('192.168.16.172', 'mmd', private_key_path, private_key_pass, files, sftp_put)
