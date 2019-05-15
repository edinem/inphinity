"""
Date: le 24/04/19

For the uses of dictionary
https://www.tutorialspoint.com/python/python_dictionary.htm
https://www.journaldev.com/23232/python-add-to-dictionary
"""

import datetime
import logging

from configuration.configuration_api import ConfigurationAPI
from projet_b11.import_databases.DomainInteraction import DomainInteraction
from rest_client.AuthenticationRest import AuthenticationAPI
from rest_client.DomainInteractionPairRest import DomainInteractionPairAPI
from rest_client.DomainInteractionSourceRest import DomainInteractionSourceAPI
from rest_client.DomainRest import DomainAPI
from rest_client.DomainSourceInformationRest import DomainSourceInformationAPI


class DomainInteractionUpdater:
    """
    Class used to get information from Inphinity database through the REST API.
    This class is used to represent domain-domain interaction and a dictionary of all domain
    """

    def __init__(self):

        # configure logger
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        self.log.addHandler(logging.StreamHandler())

        # authentication to use the REST API
        self.conf = ConfigurationAPI()
        self.conf.load_data_from_ini()
        AuthenticationAPI().createAutenthicationToken()

        # initialise a domain id to domain designation dictionary and vice versa
        self.domain_dict = {}
        self.domain_dict_reverse = {}
        self.__init_domain_dict()

        # initialise a ddi id to ddi (DomainInteraction instance) dictionary and vice versa
        self.interaction_dict = {}
        self.interaction_dict_reverse = {}
        self.__init_interaction_dict()

        # initialise a source designation to source id dictionary
        self.source_dict = {}
        self.__init_source_dict()

        # initialise a ddi source id to source id dictionary
        self.interaction_source_dict = {}
        self.__init_interaction_source_dict()

        # sets to add domains and interactions not present in Inphinity
        self.new_domains = set()
        self.new_interactions = set()

    def __init_domain_dict(self):
        """
        Retrieves all domains from Inphinity and stores them in the two corresponding dictionaries.
        """
        for domain in DomainAPI().get_all():
            self.domain_dict[domain['id']] = domain['designation']
            self.domain_dict_reverse[domain['designation']] = domain['id']
        self.log.info('Retrieved {} domains from Inphinity.'.format(len(self.domain_dict)))

    def __init_interaction_dict(self):
        """
        Retrieves all domain-domain interactions from Inphinity and stores them in the two corresponding dictionaries.
        """
        for interaction in DomainInteractionPairAPI().get_all():
            domain_a = self.domain_dict[interaction['domain_a']]
            domain_b = self.domain_dict[interaction['domain_b']]
            ddi = DomainInteraction(domain_a, domain_b)
            self.interaction_dict[interaction['id']] = ddi
            self.interaction_dict_reverse[ddi] = interaction['id']
        self.log.info('Retrieved {} domains interactions from Inphinity.'.format(len(self.interaction_dict)))

    def __init_source_dict(self):
        """
        Retrieves all sources from Inphinity and stores them in the corresponding dictionary.
        """
        for source in DomainSourceInformationAPI().get_all():
            self.source_dict[source['designation']] = source['id']
        self.log.info('Retrieved {} sources from Inphinity.'.format(len(self.source_dict)))

    def __init_interaction_source_dict(self):
        """
        Retrieves the interaction sources and stores them in the corresponding dictionary.
        """
        for interaction_source in DomainInteractionSourceAPI().get_all():
            interaction_id = interaction_source['domain_interaction']
            if self.interaction_source_dict.get(interaction_id) is None:
                self.interaction_source_dict[interaction_id] = [interaction_source['information_source']]
            else:
                self.interaction_source_dict[interaction_id].append(interaction_source['information_source'])
        self.log.info('Retrieved {} domain interaction sources from Inphinity.'.format(len(self.interaction_source_dict)))

    def __find_new_domains(self, interaction_set):
        """
        Adds to the new_domain set all domains of interaction_set that do not exists in Inphinity.

        :param interaction_set: A set of DomainInteraction
        :type interaction_set: set
        """
        self.new_domains.clear()
        for interaction in interaction_set:
            if self.domain_dict_reverse.get(interaction.first_dom) is None:
                self.new_domains.add(interaction.first_dom)
            if self.domain_dict_reverse.get(interaction.second_dom) is None:
                self.new_domains.add(interaction.second_dom)
        self.log.info('Found {} new domains.'.format(len(self.new_domains)))

    def __find_new_interactions(self, interaction_set):
        """
        Adds to the new_interactions set all interactions that do not exist in Inphinity.

        :param interaction_set: A set of DomainInteraction
        :type  interaction_set: set
        """
        self.new_interactions.clear()
        for interaction in interaction_set:
            if self.interaction_dict_reverse.get(interaction) is None:
                self.new_interactions.add(interaction)
        self.log.info('Found {} new domain interactions out of {}.'.format(len(self.new_interactions), len(interaction_set)))

    def __new_domains_to_list(self):
        """
        Returns the new_domain set as a list.

        :return: a list of new domains
        :rtype: list
        """
        return [{'designation': d} for d in self.new_domains]

    def __new_interactions_to_list(self):
        """
        Returns the new_interaction set as a list.

        :return: a list of new interactions with domain ids
        :rtype: list
        """
        return [{
            "domain_a": self.domain_dict_reverse[i.first_dom],
            "domain_b": self.domain_dict_reverse[i.second_dom]
        } for i in self.new_interactions]

    def __insert_new_domains(self):
        """
        Inserts the new domains into Inphinity and update the corresponding dictionaries.
        """
        self.log.info('Inserting new domains.')
        for domain in self.__new_domains_to_list():
            res = DomainAPI().setDomain(domain)
            self.domain_dict[res['id']] = res['designation']
            self.domain_dict_reverse[res['designation']] = res['id']

    def __insert_new_interactions(self):
        """
        Inserts the new interactions into Inphinity and update the corresponding dictionaries.
        """
        self.log.info('Inserting new domain interactions.')
        for interaction in self.__new_interactions_to_list():
            res = DomainInteractionPairAPI().setDomainInteractionPair(interaction)
            ddi = DomainInteraction(self.domain_dict[res['domain_a']], self.domain_dict[res['domain_b']])
            self.interaction_dict[res['id']] = ddi
            self.interaction_dict_reverse[ddi] = res['id']

    def __insert_new_interaction_sources(self, interaction_set, source):
        """
        Inserts interaction sources for the given interactions which do not exists for the given source.

        :param interaction_set: interactions which we may need to insert an interaction source for
        :type  interaction_set: set

        :param source: the source of the interaction
        :type  source: string
        """
        self.log.info('Inserting new domain interaction sources.')
        source_id = self.source_dict[source]
        for interaction in interaction_set:
            interaction_id = self.interaction_dict_reverse[interaction]
            current_source_ids = self.interaction_source_dict.get(interaction_id)
            if current_source_ids is None or source_id not in current_source_ids:
                res = DomainInteractionSourceAPI().setDomainInteractionSource({
                    'date_creation': datetime.date.today().__str__(),
                    'domain_interaction': interaction_id,
                    'information_source': source_id
                })
                self.interaction_source_dict[res['id']] = res['information_source']

    def update_inphinity_database(self, interaction_set, source):
        """
        Function used to update the inphinity database. It uses a set of interactions and a source (e.g. 3did).
        The function is going to find all new interactions, all new domain from them and insert the Domain, interactions
        ans interaction source.

        :param interaction_set: a set of DomainInteraction
        :type  interaction_set: set

        :param source: a string which is the database name
        :type  source: string
        """

        if self.source_dict.get(source) is None:
            raise ValueError('Source {} does not exists in Inphinity.'.format(source))

        # 1. check which domain from the given interactions do not exists in Inphinity
        self.__find_new_domains(interaction_set)

        # 2. insert those domains into Inphinity
        self.__insert_new_domains()

        # 3. check which of the given interactions do not exists in Inphinity
        self.__find_new_interactions(interaction_set)

        # 4. insert them into Inphinity (only the interaction, not the interaction source)
        self.__insert_new_interactions()

        # 5. check which of the given interactions do not have a interaction source corresponding to the given source
        self.__insert_new_interaction_sources(interaction_set, source)
        self.log.info('Done.')
