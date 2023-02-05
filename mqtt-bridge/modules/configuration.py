import configparser

CFG_NAME = 'config.ini'

config_file = configparser.ConfigParser()

def read():
    config = configparser.ConfigParser()
    config.read(CFG_NAME)
    return config