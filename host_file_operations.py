import helper


def read_file(file='hosts'):
    return get_host_credentials(helper.read_lines(file))


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
