import ftplib
import gzip
import logging
import os
import re
import shutil
from ftplib import FTP

from projet_b11.import_databases.DomainInteraction import DomainInteraction


class Pfam:
    """
    Class used to get domain-domain interaction from Pfam
    """

    # path for the current version text file
    __current_version_file = 'version_ipfam.txt'

    # FTP server address
    __server_address = 'ftp.ebi.ac.uk'

    # file that will contain all interactions
    interaction_filename = "interactions_pfam.txt"

    # temporary file to save the downloaded version numbers
    tmp_version_filename = "version_ipfam_tmp.txt"

    def __init__(self):

        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        self.log.addHandler(logging.StreamHandler())

        # create version file if it does not exists
        try:
            open(Pfam.__current_version_file, 'x')
        except FileExistsError:
            pass

        self.latest_version = None
        self.current_version = None

        try:
            self.log.info("Opening FTP connexion with {}".format(Pfam.__server_address))
            self.ftp = FTP(Pfam.__server_address)
            self.ftp.login()
        except ftplib.all_errors as e:
            self.log.error('Connexion with FTP does not work.')
            raise e
        self.domain_interactions = set()

    def __get_current_version(self):
        """
        Fetches the database version from the current version text file.
        """
        with open(Pfam.__current_version_file, 'r') as f:
            self.current_version = f.readline()
        self.log.info('Current version: {}'.format(self.current_version))

    def __get_latest_version(self):
        """
        Function used to get the Pfam database version. self.version is used to keep it.

        Pour la connexion FTP
        http://zetcode.com/python/ftp/

        Pour l'ouverture du gz
        https://stackoverflow.com/questions/48466421/python-how-to-decompress-a-gzip-file-to-an-uncompressed-file-on-disk
        """

        try:
            self.log.info("Downloading version file")
            self.ftp.retrbinary("RETR /pub/databases/Pfam/current_release/Pfam.version.gz",
                                open("./tmp.gz", "wb").write)
        except ftplib.all_errors as e:
            self.log.error("Download of the version from iPfam crashed.")
            raise e

        self.log.info("Extracting archive to {}".format(Pfam.tmp_version_filename))
        with gzip.open("./tmp.gz", 'rb') as f_in:
            with open(Pfam.tmp_version_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        self.latest_version = open(Pfam.tmp_version_filename, 'r').read()
        self.latest_version = re.findall('\\d+.\\d+', self.latest_version)[0]
        os.remove("./tmp.gz")
        os.remove(Pfam.tmp_version_filename)
        self.log.info("Latest version: {}".format(self.latest_version))

    def __save_new_version(self):
        """
        Saves the latest version into the current version text file.
        """
        with open(Pfam.__current_version_file, 'w') as f:
            f.write(self.latest_version)
        self.log.info('Saved new version {} to file.'.format(self.latest_version))

    def __fetch_interactions(self):
        """
        Function used to get all the domain-domain interactions from Pfam database.
        All the interaction are in domain_interactions.

        For fileInput
        https://bytes.com/topic/python/answers/870172-python-search-text-file-string-replace
        https://docs.python.org/2/library/fileinput.html
        """

        # Downloads of the archive
        try:
            self.ftp.retrbinary("RETR /pub/databases/Pfam/current_release/database_files/pfamA_interactions.txt.gz",
                                open("./tmp.gz", "wb").write)
        except ftplib.all_errors as e:
            self.log.error("Download of the interactions from iPfam crashed")
            raise e
        # Opening of the archive
        self.log.info("Extracting archive to {}".format(Pfam.interaction_filename))
        with gzip.open("./tmp.gz", 'rb') as f_in:
            with open(Pfam.interaction_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        # Suppression of the archive
        os.remove("./tmp.gz")
        interactions = open(Pfam.interaction_filename, 'rb')
        # We read the file line by line.
        self.log.info("Reading and creating the interactions ")
        for line in interactions.readlines():
            # Separations of both domain from the interaction
            line = line.decode('UTF-8')
            line = line.strip('\n')
            sep = line.partition('\t')
            # Instantiation of a new interaction and add it to domain_interactions
            self.domain_interactions.add(DomainInteraction(sep[0], sep[2]))
        self.log.info("All Pfam interactions done")
        os.remove(Pfam.interaction_filename)

    def has_new_version(self):
        """
        :return: True if a new version of the database if available, false otherwise
        """
        self.__get_current_version()
        self.__get_latest_version()

        if self.current_version == self.latest_version:
            self.log.info('No new version found.')
            return False
        else:
            self.log.info('New version found: {}.'.format(self.latest_version))
            return True

    def get_interactions(self):
        self.__fetch_interactions()
        if self.latest_version is not None:
            self.__save_new_version()

    def __str__(self):
        """
        Redefinition of toString so it display all the interactions in Pfam Database.
        """
        tmp = "Version : " + self.latest_version + "\n List of all interactions:\n"
        for inter in self.domain_interactions:
            tmp += inter.__str__()
        return tmp
