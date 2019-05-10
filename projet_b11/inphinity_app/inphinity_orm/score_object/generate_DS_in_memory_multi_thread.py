# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 18:53:00 2019
@author: Daniel Oliveira Paiva
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time

from django.http import HttpResponseRedirect, HttpResponse
from ..models import *
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import threading
import multiprocessing
from collections import defaultdict
import pdb
import numpy as np
from .HMM_Request import HMM_request
import json

class GenerateDS():

    def __init__(self, list_nb_bins=[], list_size_bins=[], max_value=190, list_ds=[]):
        self.nb_bins = list_nb_bins
        self.size_bins = list_size_bins
        self.max_value = max_value
        self.list_ds = list_ds

    def get_all_couples_by_level_source(self, fk_level, fk_source):
        listOfCouples = []
        couples = Couple.objects.filter(level__id = fk_level, source_data__id = fk_source)
        for couple in couples:
            listOfCouples.append(couple)
        return listOfCouples

    def get_all_Proteins_by_organism_id(self,organism_id):
        listOfProteins = []
        proteins = Protein.objects.filter(organism__id=organism_id)
        for protein in proteins:
            listOfProteins.append(protein)
        return proteins

    def get_all_DDI_interaction_to_dictionary(self):
        dictionaryOfDomainsInteraction  = defaultdict(list)
        domains = DomainInterationsPair.objects.all()
        for domain in domains:
            tuple_domains = (domain.domain_a.id, domain.domain_b.id)
            dictionaryOfDomainsInteraction[tuple_domains] = domain.id
        return dictionaryOfDomainsInteraction

    def get_all_DDI_interactionDB_to_dictionary(self):
         dict_OfDDIIntDB = defaultdict(list)
         domainsDB = DomainInteractionSource.objects.all()
         for domainDB in domainsDB:
             dict_OfDDIIntDB[domainDB.domain_interaction.id].append(domainDB.information_source.id)
         return dict_OfDDIIntDB

    def get_all_protein_domain_dict(self):
        dict_protein = defaultdict(list)
        prots = ProteinPfam.objects.all()
        for prot in prots:
            dict_protein[prot.protein.id].append(prot.domain.id)
        return dict_protein

    def get_couples_NCBI_phagesDB(self):
         list_couples = [];
         for ds in self.list_ds:
             list_couples += self.get_all_couples_by_level_source(1, ds)
         return list_couples

    def search_domains(self,protein_id):
        #values = self.dict_prot_dom.get(protein_id, [])
        values = []
        proteins = ProteinPfam.objects.filter(protein__id = protein_id)
        for protein in proteins:
                values.append(protein.domain.id)
        return protein_id, values

    def get_list_domains(self,organism_id):
        max_proce = multiprocessing.cpu_count()
        max_proce = 1
        dict_domains = {}
        list_proteins = self.get_all_Proteins_by_organism_id(organism_id)
        for protein_obj in list_proteins:
            protein_id, values = self.search_domains(protein_obj.id)
            if len(values) > 0:
                dict_domains[protein_id] = values
        return dict_domains

    def calculate_scores(self,list_db_domains):
        if 1 in list_db_domains or 2 in list_db_domains or 3 in list_db_domains:
            return 9
        else:
            return len(list_db_domains)

    def combine_domaines(self, list_dom_bact, list_dom_phage):
        list_scores_ddi = []
        id_interaction = -1
        for dom_bact in list_dom_bact:
            for dom_phage in list_dom_phage:
                id_interaction = self.dict_ddi_id_inter.get((dom_bact, dom_phage), -1)
                if id_interaction == -1:
                    id_interaction = self.dict_ddi_id_inter.get((dom_phage, dom_bact), -1)
                if id_interaction != -1:
                    # An error here TypeError("unhashable type: 'list'",)
                    list_db_domains = self.dict_interactions_ddi_db.get(id_interaction, [])
                    score_ddi = self.calculate_scores(list_db_domains)
                    list_scores_ddi.append(score_ddi)
        return list_scores_ddi

    def create_bins_scores_NB(self, list_scores_values, qty_bins, only_zeros = False):
        #Number of bins
        list_of_quantites, bins_intervals, bins_size_draw  = plt.hist(list_scores_values, bins=qty_bins)
        plt.close('all')
        if only_zeros == True:
            position = np.where(list_of_quantites != 0)
            position = position[0][0]
            list_of_quantites[0], list_of_quantites[position] = list_of_quantites[position], list_of_quantites[0]
            qty_bins = len(bins_intervals)
            bins_intervals = np.zeros(qty_bins)

        return list_of_quantites, bins_intervals


    def create_bins_scores_SB(self,list_scores_values, size_bins):
        #Size of bins
        number_bins = int(self.max_value/ size_bins)
        range_bins = (self.max_value + 0.5) / number_bins
        range_bins_vec = np.arange(0, (self.max_value + range_bins), range_bins)
        list_of_quantites, bins_intervals, bins_size_draw  = plt.hist(list_scores_values, bins=range_bins_vec)
        plt.close('all')
        return list_of_quantites, bins_intervals

    def set_id_label_couple(self,id_couple, label_couple, vec_values):
        vec_scores = np.concatenate(([id_couple], vec_values, [label_couple]), axis = 0)
        return vec_scores

    def save_DS(self,matrix_values, file_name, config_bins = False):
        nb_columns = len(matrix_values[0]) -2
        string_head = "Id_interactions,"
        format_values = "%i,"
        aux_column_number = 0
        type_info = ""
        if config_bins == False:
            type_info = "%i,"
        else:
            type_info = "%1.4f,"

        while nb_columns > aux_column_number:
            string_head += "B" + str(aux_column_number) + ","
            format_values += type_info
            aux_column_number += 1

        format_values += "%i"
        string_head += "label"

        #https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.savetxt.html
        np.savetxt(file_name, matrix_values, delimiter=',', fmt=format_values, header=string_head)

    def generate_PPI(self,couple_obj):
        print("Couple tested {0}".format(couple_obj.id))
        bacteria_id = couple_obj.bacterium.id
        phage_id = couple_obj.bacteriophage.id
        dict_bacterium = self.get_list_domains(bacteria_id)
        dict_phage = self.get_list_domains(phage_id)
        aux = 0
        list_domains_bact = []
        list_domains_phage = []
        list_scores_ppi = []
        for key_bact in dict_bacterium:
            list_domains_bact = dict_bacterium[key_bact]
            for key_phage in dict_phage:
                list_domains_phage = dict_phage[key_phage]
                list_scores = self.combine_domaines(list_domains_bact, list_domains_phage)
                list_scores_ppi = list_scores_ppi + list_scores

        for size in self.size_bins:
            bins_scores_SB, bins_size_SB = self.create_bins_scores_SB(list_scores_ppi, size)
            bins_scores_SB = self.set_id_label_couple(couple_obj.id, couple_obj.interaction_type, bins_scores_SB)
            self.lock.acquire()
            self.matrix_results_size_bins[size] = np.append(self.matrix_results_size_bins[size], [bins_scores_SB], axis = 0)
            self.lock.release()

        for nb in self.nb_bins:
            bins_scores_NB, bins_size_NB = self.create_bins_scores_NB(list_scores_ppi, nb, False)
            bins_scores_NB = self.set_id_label_couple(couple_obj.id, couple_obj.interaction_type, bins_scores_NB)
            self.lock.acquire()
            self.matrix_results_nb_bins[nb] = np.append(self.matrix_results_nb_bins[nb], [bins_scores_NB], axis = 0)
            self.lock.release()

        print("END Couple tested {0}".format(couple_obj.id))

    def launchGeneration(self):
        start = time.time()
        self.list_couples = self.get_couples_NCBI_phagesDB()

        print('End of the couples collection')
        self.dict_ddi_id_inter = self.get_all_DDI_interaction_to_dictionary()
        print('End of the DDI collection')
        self.dict_interactions_ddi_db = self.get_all_DDI_interactionDB_to_dictionary()
        print('End of the interaction DDI collection')

        self.list_domains_bact = []
        self.list_domains_phage = []
        self.list_scores_ppi = []

        self.matrix_results_size_bins = {}
        self.max_value = 190
        for size in self.size_bins:
            size_matrix = int(self.max_value / size)
            self.matrix_results_size_bins[size] = np.empty([0, (size_matrix + 2)])

        self.matrix_results_nb_bins = {}
        for nb in self.nb_bins:
            self.matrix_results_nb_bins[nb] = np.empty([0, (nb + 2)])

        self.lock = threading.Lock()
        # %% Start multiprocess pool
        max_proce = multiprocessing.cpu_count()
        print("------------------------------")
        print("you have these processores: " + str(max_proce))
        print("------------------------------")
        max_proce = max_proce - 2

        #### To do the multithread caling here
        with ThreadPoolExecutor(max_workers=max_proce) as executor:
            executor.map(self.generate_PPI, self.list_couples)



        for size in self.size_bins:
            self.save_DS(self.matrix_results_size_bins[size], './datasets/SB_' + str(size) + '_ML.csv', False)

        for nb in self.nb_bins:
            self.save_DS(self.matrix_results_nb_bins[nb], './datasets/NB_' + str(nb) + '_ML.csv', False)

        end = time.time()
        print("The script time is {0} minutes".format((end - start) / 60))
