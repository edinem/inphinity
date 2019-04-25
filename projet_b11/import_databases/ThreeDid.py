import gzip
import shutil
import subprocess

import mysql
import requests

from projet_b11.import_databases.Domain_Interaction import DomainInteraction
from projet_b11.import_databases.MySQLConfiguration import MySQLConfiguration


class ThreeDid:

    # URL which gives us the version of the 3did database
    version_url = 'https://interactome3d.irbbarcelona.org/api/getVersion'

    # do not use directly – URL where we can find the compressed SQL file
    db_url = ['https://3did.irbbarcelona.org/download/current/', '3did.sql', '.gz']

    archive_url = ''.join(db_url)
    archive_filename = ''.join(db_url[1:])
    sql_filename = db_url[1]

    def __init__(self):
        self.version = None
        self.db_cursor = None
        self.db_connection = None
        self.domain_interactions = set()
        self.init_mysql_connection()

    # initializes the mysql connection or raises an exception
    def init_mysql_connection(self):
        try:
            config = MySQLConfiguration()
            self.db_connection = mysql.connector.connect(user=config.user, host=config.host)
            self.db_cursor = self.db_connection.cursor()
        except mysql.connector.Error as e:
            print("Connexion à la base de données MySQL impossible.")
            raise e

    def close_mysql_connection(self):
        self.db_connection.close()
        self.db_cursor.close()

    # fetch the database version
    def fetch_version(self):
        self.version = requests.get(ThreeDid.version_url).content

    # download compressed SQL file to disk
    def download_archive(self):
        archive = requests.get(ThreeDid.db_url)
        open(ThreeDid.archive_filename, 'wb').write(archive.content)

    # extract compressed SQL file
    def extract_archive(self):
        with gzip.open(ThreeDid.archive_filename, 'rb') as f_in:
            with open(ThreeDid.sql_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    # import database into mysql
    # db_cursor: opened database connection
    def import_sql(self):

        # recreate database
        self.db_cursor.execute('drop database if exists 3did')
        self.db_cursor.execute('create database 3did')

        # import downloaded database
        out = subprocess.check_output(['mysql', '-u', 'root', '--show-warnings', '-e', 'use 3did; source ' + ThreeDid.sql_filename + ';'])
        print(out.decode())

    # creates DomainInteraction instances and adds them to the domain_interactions set
    def get_interactions(self):

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

        self.close_mysql_connection()
