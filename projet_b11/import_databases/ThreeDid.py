import gzip
import logging
import os
import re
import shutil

import requests

from projet_b11.import_databases.DomainInteraction import DomainInteraction


class ThreeDid:
    """
    Utility class to download the 3did database and extract the DDI.
    """

    # path for the current version text file
    __current_version_file = 'version_3did.txt'

    # URL which gives us the version of the 3did database
    __version_url = 'https://interactome3d.irbbarcelona.org/api/getVersion'

    # do not use directly – URL where we can find the file with the DDI from 3did
    __ddi_url = ['https://3did.irbbarcelona.org/download/current/', '3did_flat', '.gz']

    __archive_url = ''.join(__ddi_url)
    __archive_filename = ''.join(__ddi_url[1:])
    __ddi_filename = __ddi_url[1]

    def __init__(self):

        self.__log = logging.getLogger(__name__)
        self.__log.setLevel(logging.INFO)
        self.__log.addHandler(logging.StreamHandler())

        # create version file if it does not exists
        try:
            open(ThreeDid.__current_version_file, 'x')
        except FileExistsError:
            pass

        self.current_version = None
        self.latest_version = None
        self.domain_interactions = set()

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
        Downloads the archive containing the DDI and saves it to disk.
        """
        self.__log.info('Downloading archive at {}'.format(ThreeDid.__archive_url))
        archive = requests.get(ThreeDid.__archive_url)

        self.__log.info('Saving archive to {}'.format(ThreeDid.__archive_filename))
        with open(ThreeDid.__archive_filename, 'wb') as f:
            f.write(archive.content)

    def __extract_archive(self):
        """
        Extracts the DDI archive file.
        """
        self.__log.info('Extracting archive to {}'.format(ThreeDid.__ddi_filename))
        with gzip.open(ThreeDid.__archive_filename, 'rb') as f_in:
            with open(ThreeDid.__ddi_filename, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(ThreeDid.__archive_filename)

    def __fetch_interactions(self):
        """
        Creates DomainInteraction instances and adds them to the domain_interactions set.
        """

        with open(ThreeDid.__ddi_filename) as f:
            for line in f:
                res = re.match(r'^#=ID.*(PF\d{5})\.\d+@Pfam.*(PF\d{5})\.\d+@Pfam.*$', line)
                if res is not None:
                    domain_a, domain_b = res.groups()
                    self.domain_interactions.add(DomainInteraction(domain_a, domain_b))

        os.remove(ThreeDid.__ddi_filename)
        self.__log.info('{} domain interactions extracted.'.format(str(len(self.domain_interactions))))

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
        self.__fetch_interactions()
        if self.latest_version is not None:
            self.__save_new_version()
