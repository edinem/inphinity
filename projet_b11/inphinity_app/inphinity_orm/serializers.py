from rest_framework import serializers
from .models import *

#To add hyperlinks

class SourceDataSerializer(serializers.ModelSerializer):
    #genuses = serializers.HyperlinkedRelatedField(view_name='genus_detail', many=True, read_only=True)
    class Meta:
        model = SourceData
        fields = ('id', 'designation')

class PersonResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonResponsible
        fields = ('id', 'name')

class GeneSerializer(serializers.ModelSerializer):
    protein_gene = serializers.HyperlinkedRelatedField(view_name='protein_detail', many = True, read_only=True)
    class Meta:
        model = Gene
        fields = ('id', 'id_db_online', 'sequence_DNA', 'fasta_head', 'position_start', 'position_end', 'number_of_seq','organism','position_start_contig','position_end_contig', 'protein_gene', 'contig')

class OrganismSerializer(serializers.ModelSerializer):
    #source_data = serializers.HyperlinkedRelatedField(view_name='source_data_detail', many = False, read_only=True)
    #person_responsible = serializers.HyperlinkedRelatedField(view_name='person_responsible_detail', many = False, read_only=True)

    organism_gene = serializers.HyperlinkedRelatedField(view_name='gene_detail', many=True, read_only=True)
    organism_contig = serializers.HyperlinkedRelatedField(view_name='contig_detail', many = True, read_only=True)
    organism_wholeDNA = serializers.HyperlinkedRelatedField(view_name='wholeDNA_detail', many = True, read_only=True)
    protein_organism = serializers.HyperlinkedRelatedField(view_name='protein_detail', many = True, read_only=True)
    

    class Meta:
        model = Organism
        fields = ('acc_number', 'gi_number', 'source_data', 'person_responsible','organism_gene', 'organism_contig', 'organism_wholeDNA', 'protein_organism')
        abstract = True

class BacteriumSerializer(OrganismSerializer):
    #strain =  serializers.HyperlinkedRelatedField(view_name='strain_detail', many=False, read_only=True)
    class Meta(OrganismSerializer.Meta):
        model = Bacterium
        fields = OrganismSerializer.Meta.fields + ('id', 'strain')

class BacteriophageSerializer(OrganismSerializer):
    #baltimore_classification = serializers.HyperlinkedRelatedField(view_name='baltimore_classification_detail', many=False, read_only=True)
    class Meta(OrganismSerializer.Meta):
        model = Bacteriophage
        fields = OrganismSerializer.Meta.fields + ('id', 'baltimore_classification', 'designation')

class WholeDNASerializer(serializers.ModelSerializer):
    #organism = OrganismSerializer(many=False, read_only=True)
    #organism = serializers.HyperlinkedRelatedField(vi, many=True, read_only=True)
    class Meta:
        model = WholeDNA
        fields = ('id', 'id_db_online', 'sequence_DNA', 'fasta_head', 'organism')

class ProteinSerializer(serializers.ModelSerializer):
    position_start = serializers.CharField(allow_null = True)
    position_end = serializers.CharField(allow_null = True)
    accession_num = serializers.CharField(allow_null = True)
    id_db_online = serializers.CharField(allow_null = True)

    class Meta:
        model = Protein
        fields = ('id','gene', 'id_db_online', 'sequence_AA','fasta_head','description','accession_num','position_start','position_end', 'organism')


class ContigSerializer(serializers.ModelSerializer):
    gene_contig = serializers.HyperlinkedRelatedField(view_name='protein_detail', many = True, read_only=True)
    class Meta:
        model = Contig
        fields = ('id', 'id_db_online', 'sequence_DNA', 'fasta_head', 'organism', 'gene_contig')

class BaltimorClassificationSerializer(serializers.ModelSerializer):
    bacteriophages = BacteriophageSerializer(many=True, read_only=True)
    class Meta:
        model = BaltimoreClassification
        fields = ('id', 'designation', 'class_number', 'bacteriophages')

class StrainSerializer(serializers.ModelSerializer):
    #bacteria = BacteriumSerializer(many=True, read_only=True)
    bacteria = serializers.HyperlinkedRelatedField(view_name='bacterium_detail', many=True, read_only=True)
    class Meta:
        model = Strain
        fields = ('id', 'designation', 'specie', 'bacteria')

class SpecieSerializer(serializers.ModelSerializer):
    #strains = StrainSerializer(many=True, read_only=True)
    strains =  serializers.HyperlinkedRelatedField(view_name='strain_detail', many=True, read_only=True)
    class Meta:
        model = Specie
        fields = ('id', 'designation', 'genus', 'strains')

class GenusSerializer(serializers.ModelSerializer ):
    #species = SpecieSerializer(many=True, read_only=True)
    species = serializers.HyperlinkedRelatedField(view_name='specie_detail', many=True, read_only=True)
    class Meta:
        model = Genus
        fields = ('id','designation', 'family', 'species')

class FamilySerializer(serializers.ModelSerializer ):
    #For other type of serialization you can visit this page: http://www.tomchristie.com/rest-framework-2-docs/api-guide/relations
    #genuses = GenusSerializer(many=True, read_only=True)
    genuses = serializers.HyperlinkedRelatedField(view_name='genus_detail', many=True, read_only=True)
    class Meta:
        model = Family
        fields = ('id','designation', 'genuses')


#INformation for the couples
class InteractionValiditySerializer(serializers.ModelSerializer):

    class Meta:
        model = InteractionValidity
        fields = ('id', 'designation')
        
class LevelInteractionSerializer(serializers.ModelSerializer):

    class Meta:
        model = LevelInteraction
        fields = ('id', 'designation')


class LysisTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LysisType
        fields = ('id', 'designation')

class CoupleSerializer(serializers.ModelSerializer):
    #bacterium = BacteriumSerializer(many=False, read_only=True)
    #bacteriophage = BacteriophageSerializer(many=False, read_only=True)
    #validity = InteractionValiditySerializer(many=False, read_only=True)
    #level = LevelInteractionSerializer(many=False, read_only=True)
    #lysis = LysisTypeSerializer(many=False, read_only=True)
    #source_data = SourceDataSerializer(many=False, read_only=True)
    #person_responsible = PersonResponsibleSerializer(many=False, read_only=True)
    class Meta:
        model = Couple
        fields = ('id','bacterium', 'bacteriophage', 'interaction_type', 'level', 'lysis', 'source_data', 'person_responsible','validity' )

#DOMAINS part
class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields =('id','designation')

class DomainInteractionPairSerializer(serializers.ModelSerializer):

    #domain_a = DomainSerializer(many=False, read_only=True)
    #domain_b = DomainSerializer(many=False, read_only=True)

    class Meta:
        model = DomainInterationsPair
        fields = ('id','domain_a','domain_b')

class DomainSourceInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = DomainSourceInformation
        fields =('id','designation')

class DomainInteractionSourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = DomainInteractionSource
        fields = ('id', 'domain_interaction','information_source','date_creation')

class DomainMethodScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = DomainMethodScore
        fields = ('id', 'designation')

class DomainInteractionScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = DomainInteractionScore
        fields = ('id', 'domain_interaction','score_method','score','date_creation')

#PFAM part
class SourcePFAMSerializer(serializers.ModelSerializer):

    class Meta:
        model = SourcePFAM
        fields = ('id','designation')

class ProteinPFAMSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProteinPfam
        fields=('id', 'protein', 'domain', 'date_creation', 'source', 'person_responsible','e_value')

class PFAMMethodScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = PFAMMethodScore
        fields = ('id', 'designation')

class PPISourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PPISource
        fields = ('id','designation')

class PPISerializer(serializers.ModelSerializer):

    class Meta:
        model = PPI
        fields = ('protein_bacterium','protein_bacterophage')


class PPIInteractionSourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PPIInteractionSource
        fields = ('id', 'ppi','source','date_creation')

class PPIPFAMScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = PPIPFAMScore
        fields = ('id', 'ppi_interaction', 'pfam_method', 'score', 'date_creation')


#COGS part

class SourceCogSerializer(serializers.ModelSerializer):

    class Meta:
        model = SourceCog
        fields = ('id', 'designation')

class COGSerializer(serializers.ModelSerializer):

    class Meta:
        model = COG
        fields = ('id', 'designation')

class ProteinCogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProteinCog
        fields = ('id', 'protein','cog','date_creation','source','person_responsible')

class COGInterationPairSerializer(serializers.ModelSerializer):

    class Meta:
        model = COGInterationPair
        fields = ('id', 'cog_a', 'cog_b')

class COGSourceInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = COGSourceInformation
        fields = ('id', 'designation')

class COGInteractionSourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = COGInteractionSource
        fields = ('id', 'cogs_interaction','information_source','date_creation')

class COGMethodScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = COGMethodScore
        fields = ('id', 'designation')

class PPICogScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = PPICogScore
        fields = ('id', 'ppi_interaction','cog_method','score','date_creation')