import main
import storm
import authorized_keys
import os
import pysftp
import shutil
import host_file_operations
import connection


def read_lines(file='storm_list_main'):
    with open(file) as file_lines:
        all_lines = file_lines.readlines()
    for line in all_lines:
        for line in all_lines:
            if line == '\n':
                all_lines.remove(line)
    return all_lines


def write_to_file(to_write, file='storm_list_main'):
    main_file = open(file, 'w')
    for line in to_write:
        main_file.write(line)
    main_file.close()


def create_uploadable_file(old_name='storm_list_main', new_name='config'):
    current_directory = os.getcwd()
    shutil.copy(old_name, current_directory + "/" + new_name)


def sync_files_with_hosts(private_key):
    hosts = host_file_operations.read_file()
    files = ['authorized_keys', 'config']
    for host in hosts:
        connection.sftp_operation(host.ip, host.username, private_key, files, connection.sftp_put)
    #sftp_operation('192.168.16.172', 'mmd', private_key_path, private_key_pass, files, sftp_put)