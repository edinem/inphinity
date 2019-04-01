import requests
import gzip
import shutil
import os
import subprocess

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

    # fetch the database version
    def fetch_version(self):
        self.version = requests.get(ThreeDid.version_url).content

    # download compressed SQL file to disk
    def download_archive(self):
        archive = requests.get(ThreeDid.db_url)
        open(ThreeDid.archive_filename, 'wb').write(archive.content)

    # extract compressed SQL file
    def extract_sql(self):
        with gzip.open(ThreeDid.archive_filename, 'rb') as f_in:
            with open(ThreeDid.sql_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    # import database into mysql
    # db_cursor: opened database connection
    def import_db(self, db_cursor):

        # recreate database
        db_cursor.execute('drop database if exists 3did')
        db_cursor.execute('create database 3did')

        # import downloaded database
        out = subprocess.check_output(['mysql', '-u', 'root', '--show-warnings', '-e', 'use 3did; source ' + ThreeDid.sql_filename + ';'])
        print(out.decode())

    def print_ddi(self, db_cursor):

        db_cursor.execute('use 3did')

        sql = """select substring_index(d1.pfam_id, '.', 1),
                        substring_index(d2.pfam_id, '.', 1)
                   from ddi1
                  inner join domain d1
                     on ddi1.domain1 = d1.name
                  inner join domain d2
                     on ddi1.domain2 = d2.name;"""

        db_cursor.execute(sql)
        for d1, d2 in db_cursor.fetchall():
            print('Domaine 1 : {}, domaine 2 : {}'.format(d1, d2))
