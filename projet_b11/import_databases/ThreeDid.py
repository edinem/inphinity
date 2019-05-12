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

    # URL which gives us the version of the 3did database
    version_url = 'https://interactome3d.irbbarcelona.org/api/getVersion'

    # do not use directly – URL where we can find the compressed SQL file
    db_url = ['https://3did.irbbarcelona.org/download/current/', '3did.sql', '.gz']

    archive_url = ''.join(db_url)
    archive_filename = ''.join(db_url[1:])
    sql_filename = db_url[1]

    def __init__(self):

        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        self.log.addHandler(logging.StreamHandler())

        self.version = None
        self.db_cursor = None
        self.db_connection = None
        self.domain_interactions = set()
        self.__init_mysql_connection()

    def __init_mysql_connection(self):
        """
        Initializes the MySQL connection or raises an exception.
        """
        try:
            config = MySQLConfiguration()
            self.db_connection = mysql.connector.connect(user=config.user, host=config.host)
            self.db_cursor = self.db_connection.cursor()
        except mysql.connector.Error as e:
            self.log.error('Connexion à la base de données MySQL impossible.')
            raise e

    def __close_mysql_connection(self):
        """
        Closes the MySQL connections.
        """
        self.db_connection.close()
        self.db_cursor.close()

    def fetch_version(self):
        """
        Fetches the database version from the API.
        """
        self.version = requests.get(ThreeDid.version_url).content
        self.log.info('Got version: {}'.format(self.version))

    def download_archive(self):
        """
        Downloads the compressed SQL file and saves it to disk.
        """
        self.log.info('Downloading archive at {}'.format(ThreeDid.archive_url))
        archive = requests.get(ThreeDid.archive_url)
        self.log.info('Saving archive to {}'.format(ThreeDid.archive_filename))
        open(ThreeDid.archive_filename, 'wb').write(archive.content)

    def extract_archive(self):
        """
        Extracts the compressed SQL file.
        """
        self.log.info('Extracting archive to {}'.format(ThreeDid.sql_filename))
        with gzip.open(ThreeDid.archive_filename, 'rb') as f_in:
            with open(ThreeDid.sql_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    def import_sql(self):
        """
        Imports the SQL file into the MySQL database.
        """

        # recreate database
        self.log.info('Emptying 3did database.')
        self.db_cursor.execute('drop database if exists 3did')
        self.db_cursor.execute('create database 3did')

        # import downloaded database
        self.log.info('Importing SQL file into database.')
        subprocess.check_output(['mysql', '-u', 'root', '--show-warnings', '-e', 'use 3did; source ' + ThreeDid.sql_filename + ';'])

    def fetch_interactions(self):
        """
        Creates DomainInteraction instances and adds them to the domain_interactions set.
        """

        self.db_cursor.execute('use 3did')
        sql = """select substring_index(d1.pfam_id, '.', 1),
                        substring_index(d2.pfam_id, '.', 1)
                   from ddi1
                  inner join domain d1
                     on ddi1.domain1 = d1.name
                  inner join domain d2
                     on ddi1.domain2 = d2.name;"""

        self.db_cursor.execute(sql)
        for d1, d2 in self.db_cursor.fetchall():
            self.domain_interactions.add(DomainInteraction(d1, d2))

        self.log.info('{} domain interactions extracted.'.format(str(len(self.domain_interactions))))
        self.__close_mysql_connection()
