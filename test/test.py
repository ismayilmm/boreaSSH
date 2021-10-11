import pytest
from main_functions import main, storm, add_new_host, add_new_customer, authorized_keys
from helper_functions.ini_reader import get_test_path


@pytest.fixture
def main_test_file():
    return main.store_file('test_storm_list_main')


@pytest.fixture
def storm_test_output():
    return storm.StormHost('Host ural\n', '    hostname 192.168.16.128\n', '    user ural\n', '    port 9669\n')


@pytest.fixture
def test_host():
    return [('192.168.16.172', 'mmd', 'Mmd.123!')]


@pytest.fixture
def test_conf_file():
    return main.store_file('test_config')


def test_writing_duplicates(test_conf_file, main_test_file):
    assert main.get_unique_instances(test_conf_file, main_test_file) == main_test_file


def test_write_to_file(test_conf_file, main_test_file):
    main_storm_list = main.get_unique_instances(test_conf_file, main_test_file)
    assert main_storm_list == test_conf_file


def test_wrong_format(test_conf_file, storm_test_output):
    assert main.store_file('test_config')[0].__dict__ == storm_test_output.__dict__
