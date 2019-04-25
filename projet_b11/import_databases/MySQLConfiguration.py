import configparser


class MySQLConfiguration:

    filename = 'mysql.ini'

    def __init__(self):

        config = configparser.ConfigParser()
        config.read_file(open(MySQLConfiguration.filename))

        self.user = config['mysql']['user']
        self.password = config['mysql']['password']
        self.host = config['mysql']['host']
