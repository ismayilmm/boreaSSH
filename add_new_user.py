import authorized_keys
import main
from dataclasses import dataclass
import connection
import host_file_operations


@dataclass
class NewUser:
    ip: str
    username: str
    password: str


def get_new_user_credentials():
    ip = ''
    username = ''
    password = ''
    ip = input('Please enter ip of the new user: ')
    username = input('Please enter username of the new user: ')
    password = input('Please enter password of the new user: ')
    return NewUser(ip, username, password)


def add_user():
    new_user = get_new_user_credentials()
    connection.sftp_password_operation(new_user.ip, new_user.username, new_user.password)
    host_file_operations.add_new_host(new_user.ip, new_user.username)


if __name__ == '__main__':
    add_user()
