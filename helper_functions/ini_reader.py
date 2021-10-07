import configparser


def get_full_path(file: str):
    config = configparser.ConfigParser()
    config.read('info.ini')
    return config['Paths']['file_dir'] + file
