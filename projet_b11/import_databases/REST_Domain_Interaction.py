"""
Date: le 24/04/19

TODO separer l'insert d'interaction et l'insert d'interaction par bd
TODO -> Si on la trouve pas AVEC SOURCE on regarde si on la trouve SANS SOURCE
TODO -> Si on la trouve sans source on l'insert dans les sources
TODO -> Si on la trouve pas sans les sources on l'insert dans les non-source et les sources.

For the uses of dictionary
https://www.tutorialspoint.com/python/python_dictionary.htm
https://www.journaldev.com/23232/python-add-to-dictionary
"""

import datetime

from configuration.configuration_api import ConfigurationAPI
from projet_b11.import_databases.Domain_Interaction import DomainInteraction
from rest_client.AuthenticationRest import AuthenticationAPI
from rest_client.DomainInteractionPairRest import DomainInteractionPairAPI
from rest_client.DomainInteractionSourceRest import DomainInteractionSourceAPI
from rest_client.DomainRest import DomainAPI
from rest_client.DomainSourceInformationRest import DomainSourceInformationAPI


class RESTDomainInteraction:
    """
    Class used to get information from Inphinity database through the REST API.
    This class is used to represent domain-domain interaction and a dictionary of all domain
    """

    def __init__(self):
        self.domain_dict = dict()  # Dictionary from id to Pfam
        self.domain_dict_reverse = {}  # Dictionary from Pfam to id
        self.source_dict = dict()  # Dictionary Source string to source id
        self.interact_dict = dict()  # Dictionary from DDI id to DDI
        self.interact_dict_reverse = dict()  # Dictionary from DDI to DDI id
        self.domain_interactions = set()  # Set of all interactions
        self.domain_interactions_source = dict()  # Dictionary from DDI id to DDI source

        self.new_domain = set()  # Set for all the new domain we need to insert
        self.new_interactions = set()  # Set for all the new interactions we want to insert

        # authentication to use the REST API
        self.conf = ConfigurationAPI()
        self.conf.load_data_from_ini()
        AuthenticationAPI().createAutenthicationToken()

    def get_domain_dict(self):
        """
        Retrieves all domains from the Inphinity database and stores them in a dictionary.
        """
        for domain in DomainAPI().get_all():
            self.domain_dict.update({domain["id"]: domain["designation"]})
            self.domain_dict_reverse.update({domain["designation"]: domain["id"]})

    def get_domain_inter(self):
        """
        Retrieves all domain-domain interactions from the Inphinity database and stores them in a set.
        """
        for interaction in DomainInteractionPairAPI().get_all():
            # Creation of the new interaction
            domain_a = self.domain_dict.get(interaction['domain_a'])
            domain_b = self.domain_dict.get(interaction['domain_b'])
            ddi = DomainInteraction(domain_a, domain_b)
            self.domain_interactions.add(ddi)
            self.interact_dict.update({interaction['id']: ddi})
            self.interact_dict_reverse.update({ddi: interaction['id']})

    def get_inter_source(self):
        """
        Retrieves the interactions sources and stores them in a dictionary.
        """
        for interaction in DomainInteractionSourceAPI().get_all():
            interaction_id = self.interact_dict_reverse.get(interaction['domain_interaction'])
            self.domain_interactions_source.update({interaction_id: interaction['information_source']})

    def find_new_domain(self, interaction_set):
        """
        For all the interactions in the given set, adds to the new_domain dictionary all domains that do not exists in
        the Inphinity database.

        :param interaction_set: A set of interactions with potential new domains
        :type interaction_set: set - required
        """
        for interaction in interaction_set:
            if interaction.first_dom not in self.domain_dict.values() and interaction.second_dom not in self.new_domain:
                self.new_domain.add({interaction.first_dom})
            if interaction.second_dom not in self.domain_dict.values() and interaction.second_dom not in self.new_domain:
                self.new_domain.add({interaction.second_dom})

    def new_domain_to_data(self):
        """
        Returns the new_domain dictionary as a list.

        :return: The domain list
        :rtype: list
        """
        domain_list = list()
        for pfam in self.new_domain:
            domain_list.append({"designation": pfam})
        return domain_list

    def find_new_interactions(self, interaction_set):
        """
        Finds interactions that do not exist in the Inphinity database and adds them to new_interactions.

        :param interaction_set: A set of potentially new interactions
        :type  interaction_set: set
        """
        for interaction in interaction_set:
            if self.interact_dict_reverse.get(interaction) is None:
                self.new_interactions.add(interaction)

    def new_interaction_to_data(self):
        """
        Returns the new_interaction dictionary as a list.

        :return: The interaction list
        :rtype: list
        """
        interactions_list = list()
        for interact in self.new_interactions:
            interactions_list.append({
                "domain_a": self.domain_dict_reverse.get(interact.first_dom),
                "domain_b": self.domain_dict_reverse.get(interact.second_dom)})
        return interactions_list

    def update_inphinity_database(self, interaction_set, source):
        """
        Function used to update the inphinity database. It uses a set of interactions and a source (e.g. 3did).
        The function is going to find all new interactions, all new domain from them and insert the Domain, interactions
        ans interaction source.

        :param interaction_set: A set containing all interactions.
        :type  interaction_set: set - required

        :param source: A string which is the database name.
        :type  source: String - required
        """

        # 1. check which domain from the given interactions do not exists in Inphinity
        self.find_new_domain(interaction_set)

        # 2. insert those domains into Inphinity
        self.insert_new_domain()

        # 3. check which of the given interactions do not exists in Inphinity
        self.find_new_interactions(interaction_set)

        # 4. insert them into Inphinity (only the interaction, not the interaction source)
        self.insert_new_interaction()

        # 5. check which of the given interactions do not have a interaction source corresponding to the given source
        self.insert_new_interaction_source(interaction_set, source)

    def insert_new_domain(self):
        """
        Inserts the new domains into the Inphinity database and update domain dictionary.
        """
        for domain in self.new_domain_to_data():
            new_id = DomainAPI().setDomain(domain)
            self.domain_dict.update({new_id: domain["designation"]})
            self.domain_dict_reverse.update({domain["designation"]: new_id})

    def insert_new_interaction(self):
        """
        Inserts the new interactions into the Inphinity database and update interaction dictionary.
        """
        for interaction in self.new_interaction_to_data():
            interaction_id = DomainInteractionPairAPI().setDomainInteractionPair(interaction)
            ddi = DomainInteraction(interaction.domain_a, interaction.domain_b)
            self.interact_dict.update({interaction_id: ddi})
            self.interact_dict_reverse.update({ddi: interaction})

    def insert_new_interaction_source(self, interaction_set, source):
        """
        Inserts interaction sources which do not exists.

        :param interaction_set: interactions which we may need to insert an interaction source for
        :type interaction_set: set
        :param source: the source of the interaction
        :type source: string
        """
        for interaction in interaction_set:
            interaction_id = self.interact_dict_reverse.get(interaction)
            current_source = self.domain_interactions_source.get(interaction_id)
            if current_source is None or current_source != source:
                DomainInteractionSourceAPI().setDomainInteractionSource({
                    "date_creation": datetime.datetime.now(),
                    "domain_interaction": interaction_id,
                    "source": self.source_dict.get(source)})

    def find_all_source(self):
        """
        Creates a mapping between a source's name and its database id.
        """
        for source in DomainSourceInformationAPI().get_all():
            self.source_dict.update({source["designation"]: source["id"]})
