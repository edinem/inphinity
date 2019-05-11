import datetime

from configuration.configuration_api import ConfigurationAPI
from projet_b11.import_databases.Domain_Interaction import DomainInteraction
from rest_client.AuthenticationRest import AuthenticationAPI
from rest_client.DomainInteractionPairRest import *
from rest_client.DomainInteractionSourceRest import *
from rest_client.DomainRest import *
from rest_client.DomainSourceInformationRest import *

"""
Date: le 24/04/19

"""
#TODO separer l'insert d'interaction et l'insert d'interaction par bd
#TODO -> Si on la trouve pas AVEC SOURCE on regarde si on la trouve SANS SOURCE
#TODO -> Si on la trouve sans source on l'insert dans les sources
#TODO -> Si on la trouve pas sans les sources on l'insert dans les non-source et les sources.

# https://www.tutorialspoint.com/python/python_dictionary.htm
# https://www.journaldev.com/23232/python-add-to-dictionary
# For the uses of dictionary


class RESTDomainInteraction:
    """
    Class used to get information from Inphinity database through the REST API.
    This class is used to represent domain-domain interaction and a dictionary of all domain
    """

    def __init__(self):
        self.domain_dict = dict()                 # Dictionary from id to Pfam
        self.domain_dict_reverse = {}             # Dictionary from Pfam to id
        self.source_dict = dict()                 # Dictionary Source String to source id
        self.interact_dict = dict()               # Dictionary from DDI id to DDI
        self.interact_dict_reverse = dict()       # Dictionary from DDI to DDI id
        self.domain_interactions = set()          # Set of all interactions
        self.domain_interactions_source = list()  # Set of all interactions with source
        self.new_domain = set()                   # Set for all the new domain we need to insert

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
            interact = self.interact_dict_reverse.get(interaction['domain_interaction'])
            self.domain_interactions_source.append({interact, interaction['information_source']})

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

        :return: the domain list
        :rtype: list
        """
        domain_list = list()
        for pfam in self.new_domain:
            domain_list.append({"designation": pfam})
        return domain_list

    def new_interaction_to_data(self, interaction_set):
        """
        Returns the given interaction set as a list.

        :param interaction_set: All new interactions
        :type interaction_set: set - required

        :return: The interaction set as a list
        :rtype: list
        """
        interactions_list = list()
        for interact in interaction_set:
            interactions_list.append({
                "domain_a": self.domain_dict_reverse.values(interact.first_dom),    # TODO get?
                "domain_b": self.domain_dict_reverse.values(interact.second_dom)})  # TODO get?
        return interactions_list

    def insert_new_interaction(self, interact_data, source):
        """
        Inserts into the Inphinity database all interaction of the given interact_data list for the given source.

        :param interact_data: A list of interactions to insert into the Inphinity database
        :type  interact_data: list

        :param source: The source of the interaction to insert (e.g. iPfam, 3did)
        :type  source: string
        """
        for interact in interact_data:
            interact_id = DomainInteractionPairAPI().setDomainInteractionPair(interact)
            DomainInteractionSourceAPI().setDomainInteractionSource({
                "date_creation": datetime.date.today(),
                "domain_interaction": interact_id,
                "source": self.source_dict.get(source)})

    def update_inphinity_database(self, set_interaction, source):
        """
        Function used to update the inphinity database. It uses a set of interactions and a source (e.g. 3did).
        The function is going to find all new interactions, all new domain from them and insert the Domain, interactions
        ans interaction source.

        :param set_interaction: A set containing all interactions.
        :type set_interaction: set - required

        :param source: A string which is the database name.
        :type source: String - required
        """
        # TODO Faire appel a toutes les autres méthodes pour que on puisse utiliser que celle la depuis un nouveau set.
        # TODO Pour le moment on n'a que insert_new_ineraction qui fait l'insert SI l'ineract est nul part, il faut gérer les cas
        # TODO Ou l'interaction et deja présente mais pas dans la table avec la source pour laquelle on recherche.
        pass

    def insert_new_domain(self):
        """
        Inserts the new domains into the Inphinity database.
        """
        for domain in self.new_domain_to_data():
            new_id = DomainAPI().setDomain(domain)
            self.domain_dict.update({new_id: domain["designation"]})
            self.domain_dict_reverse.update({domain["designation"]: new_id})

    def find_all_source(self):
        """
        Creates a mapping between a source's name and its database id.
        """
        for source in DomainSourceInformationAPI().get_all():
            self.source_dict.update({source["designation"]: source["id"]})
