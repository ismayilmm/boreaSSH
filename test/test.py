import pytest
import main


@pytest.fixture
def main_test_file():
    return main.store_file('test_storm_list_main')


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


def test_wrong_format(test_conf_file, main_test_file):
    #test the right format

