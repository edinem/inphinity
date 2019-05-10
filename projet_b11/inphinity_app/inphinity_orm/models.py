from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
#Tables for sources

class SourceData(models.Model):
    designation = models.TextField(unique=True, blank=False)

    def __str__(self):
        return self.designation

class PersonResponsible(models.Model):
    name = models.TextField(unique=True, blank=False)

    def __str__(self):
        return self.name

#Tables for taxonomy
class Family(models.Model):
    designation = models.TextField(unique=True, blank=False)

    def __str__(self):
        return self.designation

    class Meta:
        ordering = ('designation',)

class Genus(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='genuses')
    designation = models.TextField(blank=False)

    class Meta:
        unique_together = ('family','designation')

    def __str__(self):
        return self.designation

class Specie(models.Model):
    genus = models.ForeignKey(Genus, on_delete=models.CASCADE, related_name='species')
    designation = models.TextField(blank=False)

    class Meta:
        unique_together  = ('genus','designation')

    def __str__(self):
        return self.designation

class Strain(models.Model):
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, related_name = 'strains')
    designation = models.TextField(unique=True, blank=False)

    class Meta:
        unique_together  = ('specie','designation')

    def __str__(self):
        return self.designation

#Tables related with viruses
class BaltimoreClassification(models.Model):
    class_number = models.IntegerField(unique=True, blank=False)
    designation = models.TextField(unique=True, blank=False)

    def __str__(self):
        return self.designation

#Tables related with organisms
#Organisms---
class Organism(models.Model):
    source_data = models.ForeignKey(SourceData, on_delete=models.SET_NULL, null=True, related_name='source_data')
    person_responsible = models.ForeignKey(PersonResponsible, on_delete=models.SET_NULL, null=True, related_name='person_responsible')
    acc_number = models.TextField(null=True, max_length=50)
    gi_number= models.TextField(unique=True, null=True, max_length=50)

    def __str__(self):
        return self.acc_number



class Bacterium(Organism):
    strain = models.ForeignKey(Strain, on_delete=models.CASCADE, related_name='bacteria')

    def __str__(self):
        return self.strain.designation


class Bacteriophage(Organism):
    baltimore_classification = models.ForeignKey(BaltimoreClassification, on_delete=models.SET_NULL, null=True, related_name='baltimore_classification')
    designation = models.TextField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.designation
#Organisms---END
#Composition of the organism---


class Contig(models.Model):
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE, related_name='organism_contig')
    id_db_online = models.TextField(null=True)
    sequence_DNA = models.TextField()
    fasta_head = models.TextField(null=True)

    def __str__(self):
        return self.id_db_online

class Gene(models.Model):
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE, related_name='organism_gene')
    
    contig = models.ForeignKey(Contig, on_delete=models.CASCADE, null=True, related_name='gene_contig')
    id_db_online = models.TextField(null=True)
    sequence_DNA = models.TextField()
    fasta_head = models.TextField(null=True)
    position_start = models.PositiveIntegerField(null=True)
    position_end = models.PositiveIntegerField(null=True)
    number_of_seq = models.PositiveIntegerField(null=True)
    position_start_contig = models.PositiveIntegerField(null=True, blank=True, default=None)
    position_end_contig = models.PositiveIntegerField(null=True, blank=True, default=None)
    description = models.TextField(null = True)

    def __str__(self):
        return self.id_db_online

class Protein(models.Model):
    gene = models.ForeignKey(Gene, on_delete=models.SET_NULL, related_name='protein_gene', null=True)
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE, related_name= 'protein_organism')
    id_db_online = models.TextField(null=True)
    sequence_AA = models.TextField()
    fasta_head = models.TextField(null=True)
    description = models.TextField(null = True)
    accession_num = models.TextField(null = True)
    position_start = models.PositiveIntegerField(null=True)
    position_end = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.id_db_online

class WholeDNA(models.Model):
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE, related_name='organism_wholeDNA')
    id_db_online = models.TextField(null=True)
    sequence_DNA = models.TextField()
    fasta_head = models.TextField(null=True)

    def __str__(self):
        return self.id_db_online

#Composition ot the organism--- END
#COUPLE ---
class InteractionValidity(models.Model):
    designation = models.TextField(unique=True, blank=False)

    def __str__(self):
        return self.designation

class LevelInteraction(models.Model):
    designation = models.TextField(unique=True, blank=False)

    def __str__(self):
        return self.designation

class LysisType(models.Model):
    designation = models.TextField(unique=True, blank=False)

    def __str__(self):
        return self.designation

class Couple(models.Model):
    bacterium = models.ForeignKey(Bacterium, on_delete=models.CASCADE)
    bacteriophage = models.ForeignKey(Bacteriophage, on_delete=models.CASCADE)
    validity = models.ForeignKey(InteractionValidity, on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey(LevelInteraction, on_delete=models.PROTECT)
    lysis = models.ForeignKey(LysisType, on_delete=models.SET_NULL, null=True)
    source_data = models.ForeignKey(SourceData, on_delete=models.PROTECT)
    person_responsible = models.ForeignKey(PersonResponsible, on_delete=models.PROTECT)
    interaction_type = models.BooleanField()

    class Meta:
        unique_together = ('bacterium', 'bacteriophage',)
#COUPLE --- END


#DOMAINS
class Domain(models.Model):
    designation = models.TextField(max_length=10, unique=True)

    def __str__(self):
        return self.designation

class DomainInterationsPair(models.Model):
    domain_a = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='DomainInterationsPair_domainA')
    domain_b = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name='DomainInterationsPair_domainB')

    def clean(self):
        direct = DomainInterationsPair.objects.filter(domain_a = self.domain_a, domain_b = self.domain_b)
        reverse = DomainInterationsPair.objects.filter(domain_a = self.domain_b, domain_b = self.domain_a)

        if direct.exists() or reverse.exists():
            domain_a_desc = self.domain_a.designation
            domain_b_desc = self.domain_b.designation
            raise ValidationError(
                'The pair of domains %(domain_a_desc)s - %(domain_b_desc)s already exists',
                                  params = {
                                      'domain_a_desc': domain_a_desc,
                                      'domain_b_desc' : domain_b_desc
                                      })

    class Meta:
        unique_together =('domain_a','domain_b',)



    def __str__(self):
        return (self.domain_a.designation + ' - ' + self.domain_b.designation)

class DomainSourceInformation(models.Model):
    designation = models.TextField(unique=True)

    def __str__(self):
        return self.designation

class DomainInteractionSource(models.Model):
    domain_interaction = models.ForeignKey(DomainInterationsPair, on_delete=models.CASCADE)
    information_source = models.ForeignKey(DomainSourceInformation, on_delete=models.PROTECT)
    date_creation = models.DateField(default=timezone.now, editable=True, blank=False)

    class Meta:
        unique_together = ('domain_interaction','information_source')

class DomainMethodScore(models.Model):
    designation = models.TextField(unique=True)

    def __str__(self):
        return self.designation

class DomainInteractionScore(models.Model):
    domain_interaction = models.ForeignKey(DomainInterationsPair, on_delete=models.CASCADE)
    score_method = models.ForeignKey(DomainMethodScore, on_delete=models.PROTECT)
    score = models.FloatField()
    date_creation = models.DateField(default=timezone.now, editable=True, blank=False)

    def __str__(self):
        return ('(' + str(self.domain_interaction) + ') - ' + str(self.score_method) + ' - ' + str(self.score))


#DOMAINS---END
#Prot pFAM
class SourcePFAM(models.Model):
    designation = models.TextField(unique=True)

    def __str__(self):
        return self.designation


class ProteinPfam(models.Model):
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    date_creation = models.DateField(default=timezone.now, editable=True, blank=False)
    source = models.ForeignKey(SourcePFAM, on_delete=models.PROTECT)
    person_responsible = models.ForeignKey(PersonResponsible, on_delete=models.PROTECT)
    e_value = models.FloatField(null=False)

class PFAMMethodScore(models.Model):
    designation = models.TextField(unique=True)

    def __str__(self):
        return self.designation

class PPISource(models.Model):
    designation = models.TextField(unique=True)

    def __str__(self):
        return self.designation

class PPI(models.Model):
    protein_bacterium = models.ForeignKey(Protein, on_delete=models.CASCADE, related_name='PPI_bacterium')
    protein_bacterophage = models.ForeignKey(Protein, on_delete=models.CASCADE, related_name='PPI_bacteriophage')

    class Meta:
        unique_together = ('protein_bacterium', 'protein_bacterophage',)

    def __str__(self):
        return (self.protein_bacterium.id_db_online + ' - ' + self.protein_bacterophage.id_db_online)

class PPIInteractionSource(models.Model):
    ppi = models.ForeignKey(PPI, on_delete=models.CASCADE)
    source = models.ForeignKey(PPISource, on_delete=models.PROTECT)
    date_creation = models.DateField(default=timezone.now, editable=True, blank=False)

    def __str__(self):
        return ('(' + str(self.ppi) + ') - ' + self.source.designation)



class PPIPFAMScore(models.Model):
    ppi_interaction = models.ForeignKey(PPI, on_delete=models.CASCADE)
    pfam_method = models.ForeignKey(PFAMMethodScore, on_delete=models.PROTECT)
    score = models.FloatField()
    date_creation = models.DateField(default=timezone.now, editable=True, blank=False)

    def __str__(self):
        return ('(' + str(self.ppi_interaction) + ') - ' + str(self.pfam_method) + ' - ' + str(self.score))

    class Meta:
        unique_together = ('ppi_interaction', 'pfam_method',)

#Prot pFAM---END
#COGS
class SourceCog(models.Model):
    designation = models.TextField(unique=True)

    def __str__(self):
        return self.designation


class COG(models.Model):
    designation = models.TextField(max_length=12, unique=True)

    def __str__(self):
        return self.designation

class ProteinCog(models.Model):
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)
    cog = models.ForeignKey(COG, on_delete=models.CASCADE)
    date_creation = models.DateField(default=timezone.now, editable=True, blank=False)
    source = models.ForeignKey(SourceCog, on_delete=models.PROTECT)
    person_responsible = models.ForeignKey(PersonResponsible, on_delete=models.PROTECT)

    def __str__(self):
        return (str(self.protein) + ' - ' + str(self.cog))

    class Meta:
        unique_together = ('protein', 'cog',)

class COGInterationPair(models.Model):
    cog_a = models.ForeignKey(COG, on_delete=models.CASCADE, related_name='COGSInterationPair_domainA')
    cog_b = models.ForeignKey(COG, on_delete=models.CASCADE, related_name='COGSInterationPair_domainB')

    def __str__(self):
        return (str(self.cog_a) + ' - ' + str(self.cog_b))

    def clean(self):
            direct = COGInterationPair.objects.filter(cog_a = self.cog_a, cog_b = self.cog_b)
            reverse = COGInterationPair.objects.filter(cog_a = self.cog_b, cog_b = self.cog_a)

            if direct.exists() or reverse.exists():
                cog_a_desc = self.cog_a.designation
                cog_b_desc = self.cog_b.designation
                raise ValidationError(
                    'The pair of cogs %(cog_a_desc)s - %(cog_b_desc)s already exists',
                                      params = {
                                          'cog_a_desc': cog_a_desc,
                                          'cog_b_desc' : cog_b_desc
                                          })

    class Meta:
        unique_together = ('cog_a', 'cog_b',)

class COGSourceInformation(models.Model):
    designation = models.TextField(unique=True)

    def __str__(self):
        return self.designation

class COGInteractionSource(models.Model):
    cogs_interaction = models.ForeignKey(COGInterationPair, on_delete=models.CASCADE)
    information_source = models.ForeignKey(COGSourceInformation, on_delete=models.PROTECT)
    date_creation = models.DateField(default=timezone.now, editable=True, blank=False)

    class Meta:
        unique_together = ('cogs_interaction', 'information_source',)

    def __str__(self):
        return (str(self.cogs_interaction) + ' : ' + str(self.information_source))


class COGMethodScore(models.Model):
    designation = models.TextField(unique=True)

    def __str__(self):
        return self.designation


class PPICogScore(models.Model):
    ppi_interaction = models.ForeignKey(PPI, on_delete=models.CASCADE)
    cog_method = models.ForeignKey(COGMethodScore, on_delete=models.PROTECT)
    score = models.FloatField()
    date_creation = models.DateField(default=timezone.now, editable=True, blank=False)

    def __str__(self):
        return (str(self.ppi_interaction) + ' : ' + str(self.score))