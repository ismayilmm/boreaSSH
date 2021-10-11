import configparser

config = configparser.ConfigParser()
config.read('info.ini')


def get_full_path(file: str):
    return config['Paths']['file_dir'] + file


def get_test_path(file: str):
    return config['Paths']['test_file_dir'] + file
