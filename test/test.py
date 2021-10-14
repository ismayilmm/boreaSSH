import pytest
from main_functions import storm, add_new_host, add_new_customer, authorized_keys
from helper_functions.ini_reader import get_test_path


@pytest.fixture
def main_key_file():
    return authorized_keys.read_authorized_keys_file(get_test_path('main_file_for_keys_test'))


@pytest.fixture
def main_test_file():
    return storm.store_config_file(get_test_path('test_storm_list_main'))


@pytest.fixture
def storm_input():
    return storm.store_config_file(get_test_path('test_config'))


@pytest.fixture
def storm_test_output():
    return storm.StormHost('Host ural\n', '    hostname 192.168.16.128\n', '    user ural\n', '    port 9669\n')


@pytest.fixture
def test_add_host():
    return storm.StormHost('Host miyav\n', '    hostname 192.168.31.69\n', '    user miyav\n', '    port 22\n')


@pytest.fixture
def auth_key_test_output():
    return authorized_keys.AuthorizedKey('ssh-rsa', 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDWLk1S+I6qytnkr9aLPp8SV7WzgN'
                                                    'KTBznwXUNMkscRXeRyeiyTx7e6SOaPA+/2RdB1OJc8r/m8JaJ3+Y3l1pO58SdhpDnQ'
                                                    'mCa4keJ8uRR9bk0RSLESa164tUQvNwiy7MfC0BA7YcEZCaYhiloc19BN6WLDykPRMi'
                                                    'd3M/5zqs1qARHxJtwHIDmWR9tXCZnIU30OuLZbAQeBaJknLdDXXx7ZHQLYljEih8NZ'
                                                    '5BR1SFe1jWz+JNe4YR0mV6RvRGuOyA1iXafgFGgNsbftpjKYtmUg3lo7AjEz6Pkidr'
                                                    'Q7ieWtHbT/YRSLYQ33JVPOBZ9VTUPGjlajT4rX6g7XscQopLECmrdrF7axrqUUYf7Z'
                                                    'hNBVr3h6K1Sns4oDVL4XPBsD5xGz7ryNz47/xktxe9fT73pa+X7ENFlE9hpr25kEf6'
                                                    'Us7e2vgVcwKb0cOt+SYjLJc87tIkmpxjWd+BB0JRjU3HwPXwOGF58gkTEL48Ovdbsz'
                                                    'EkQ0PCqko0i4lNcxdDtzsC8=', 'emre@manjo')


@pytest.fixture
def test_host():
    return [('192.168.16.171', 'berk', 'Vt.123!')]


@pytest.fixture
def test_conf_file():
    return storm.store_config_file(get_test_path('test_config'))


""" 
TC-1 
input: config_file with extra lines
expected output: only host is added to main file 
"""


def test_config_main(main_test_file, storm_test_output, storm_input):
    assert storm.get_unique_instances_of_config_file(storm_input, main_test_file) == storm_test_output

"""
TC-2
input: same input file as in TC-1. 
expected output: only one instance in main file 
"""


def test_writing_duplicates(storm_input, main_test_file):
    assert storm.get_unique_instances_of_config_file(storm_input, main_test_file) == main_test_file


"""
TC-3 
input: authorized_keys file with extra lines and "\n" lines. 
expected output: only proper line with key is added to main file
"""


def test_authorized_keys_write_to_file(main_key_file, auth_key_test_output):
    assert authorized_keys.get_unique_instances_of_authorized_keys(main_key_file, get_test_path('authorized_keys')) == \
           auth_key_test_output


"""
TC-4
input: same authorized_keys file with extra lines and '\n'.
expected output: 
"""





"""
TC-5
input: new customer credentials
expected output: add credentials to storm list
"""


def test_add_new_customer():
    storm.add_new_host('alias', '192.168.31.68', 'uname', '22', get_test_path('test_config'))



"""
TC-6
input: new host credentials
expected output: new host credentials are added to storm list and authorized key of host is added to authorized keys file
"""


def test_add_new_host(test_add_host):
    storm.add_new_host('miyav', '192.168.31.69', 'miyav', '22', file=get_test_path('test_config'))
    assert storm.store_config_file(get_test_path('test_config')) == test_add_host
