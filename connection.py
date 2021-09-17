import pysftp


def port_no(username):
    return 9669 if username == 'ural' else 22


def connection_options():
    """
    Note
    """
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    return cnopts


def sftp_operation(ip, username, private_key, files, sftp_function):
    with pysftp.Connection(host=ip, username=username, private_key=private_key.path,
                           private_key_pass=private_key.pass_phrase, port=port_no(username),
                           cnopts=connection_options()) as sftp:
        with sftp.cd('/home/' + username + '/.ssh'):
            for file in files:
                sftp_function(file, sftp, username)
    sftp.close()


def sftp_password_operation(ip, username, password):
    with pysftp.Connection(host=ip, username=username, password=password) as sftp:
        with sftp.cd('/home/' + username + '/.ssh'):
            sftp.put('authorized_keys')
    sftp.close()


def sftp_get(file, sftp, username):
    with sftp.cd('/home/' + username + '/.ssh'):
        sftp.get(file)


def sftp_put(file, sftp, username):
    with sftp.cd('/home/' + username + '/.ssh'):
        sftp.put(file)
