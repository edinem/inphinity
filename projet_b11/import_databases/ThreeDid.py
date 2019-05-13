import gzip
import logging
import shutil
import subprocess

import mysql.connector
import requests

from projet_b11.import_databases.DomainInteraction import DomainInteraction
from projet_b11.import_databases.MySQLConfiguration import MySQLConfiguration


class ThreeDid:
    """
    Utility class to download the 3did database and extract the DDI.
    """

    # path for the current version text file
    __current_version_file = 'version_3did.txt'

    # URL which gives us the version of the 3did database
    __version_url = 'https://interactome3d.irbbarcelona.org/api/getVersion'

    # do not use directly – URL where we can find the compressed SQL file
    __db_url = ['https://3did.irbbarcelona.org/download/current/', '3did.sql', '.gz']

    __archive_url = ''.join(__db_url)
    __archive_filename = ''.join(__db_url[1:])
    __sql_filename = __db_url[1]

    def __init__(self):

        self.__log = logging.getLogger(__name__)
        self.__log.setLevel(logging.INFO)
        self.__log.addHandler(logging.StreamHandler())

        # init MySQL connection
        self.__db_cursor = None
        self.__db_connection = None
        self.__init_mysql_connection()

        # create version file if it does not exists
        try:
            open(ThreeDid.__current_version_file, 'x')
        except FileExistsError:
            pass

        self.current_version = None
        self.latest_version = None
        self.domain_interactions = set()

    def __init_mysql_connection(self):
        """
        Initializes the MySQL connection or raises an exception.
        """
        try:
            config = MySQLConfiguration()
            self.__db_connection = mysql.connector.connect(user=config.user, host=config.host)
            self.__db_cursor = self.__db_connection.cursor()
        except mysql.connector.Error as e:
            self.__log.error('Connexion à la base de données MySQL impossible.')
            raise e

    def __close_mysql_connection(self):
        """
        Closes the MySQL connections.
        """
        self.__db_connection.close()
        self.__db_cursor.close()

    def __get_current_version(self):
        """
        Fetches the database version from the current version text file.
        """
        with open(ThreeDid.__current_version_file, 'r') as f:
            self.current_version = f.readline()
        self.__log.info('Current version: {}'.format(self.current_version))

    def __get_latest_version(self):
        """
        Fetches the database version from the API.
        """
        self.latest_version = requests.get(ThreeDid.__version_url).content.decode('ascii')
        self.__log.info('Latest version: {}'.format(self.latest_version))

    def __save_new_version(self):
        """
        Saves the latest version into the current version text file.
        """
        with open(ThreeDid.__current_version_file, 'w') as f:
            f.write(self.latest_version)
        self.__log.info('Saved new version {} to file.'.format(self.latest_version))

    def __download_archive(self):
        """
        Downloads the compressed SQL file and saves it to disk.
        """
        self.__log.info('Downloading archive at {}'.format(ThreeDid.__archive_url))
        archive = requests.get(ThreeDid.__archive_url)

        self.__log.info('Saving archive to {}'.format(ThreeDid.__archive_filename))
        with open(ThreeDid.__archive_filename, 'wb') as f:
            f.write(archive.content)

    def __extract_archive(self):
        """
        Extracts the compressed SQL file.
        """
        self.__log.info('Extracting archive to {}'.format(ThreeDid.__sql_filename))
        with gzip.open(ThreeDid.__archive_filename, 'rb') as f_in:
            with open(ThreeDid.__sql_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    def __import_sql(self):
        """
        Imports the SQL file into the MySQL database.
        """

        # recreate database
        self.__log.info('Emptying 3did database.')
        self.__db_cursor.execute('drop database if exists 3did')
        self.__db_cursor.execute('create database 3did')

        # import downloaded database
        self.__log.info('Importing SQL file into database.')
        subprocess.check_output(
            ['mysql', '-u', 'root', '--show-warnings', '-e', 'use 3did; source ' + ThreeDid.__sql_filename + ';'])

    def __fetch_interactions(self):
        """
        Creates DomainInteraction instances and adds them to the domain_interactions set.
        """

        self.__db_cursor.execute('use 3did')
        sql = """select substring_index(d1.pfam_id, '.', 1),
                        substring_index(d2.pfam_id, '.', 1)
                   from ddi1
                  inner join domain d1
                     on ddi1.domain1 = d1.name
                  inner join domain d2
                     on ddi1.domain2 = d2.name;"""

        self.__db_cursor.execute(sql)
        for d1, d2 in self.__db_cursor.fetchall():
            self.domain_interactions.add(DomainInteraction(d1, d2))

        self.__log.info('{} domain interactions extracted.'.format(str(len(self.domain_interactions))))
        self.__close_mysql_connection()

    def has_new_version(self):
        """
        :return: True if a new version of the database if available, false otherwise
        """
        self.__get_current_version()
        self.__get_latest_version()

        if self.current_version == self.latest_version:
            self.__log.info('No new version found.')
            return False
        else:
            self.__log.info('New version found: {}.'.format(self.latest_version))
            return True

    def get_interactions(self):
        """
        Downloads the database and extracts the domain-domain interactions.
        """
        self.__download_archive()
        self.__extract_archive()
        self.__import_sql()
        self.__fetch_interactions()
        self.__save_new_version()
