from HMM_request import HMM_request
from protein_request import protein_request


class score_calculation:
    interactions = [[],[]]

    def __init__(self, interactions):
        self.interactions = interactions



    def calculateScoreBetweenTwoProt(self,domainsProtA, domainsProtB):
        indexProtA = 0
        indexProtB = 0
        score = 0;

        while indexProtA < len(domainsProtA):
            while indexProtB < len(domainsProtB):
                try:
                    index = self.interactions.index(domainsProtA[indexProtA] + domainsProtB[indexProtB])

                    #VERIFIER LA SOURCE

                    score += 1;
                except:
                    print("No ineraction found between" + domainsProtA[indexProtA] + domainsProtB[indexProtB])





    def calculateScoreBetweenOneBacteryAndOnePhage(self, bacterie, phage):

        bactProteins = protein_request(bacterie)
        phageProteins = protein_request(phage)

        indexBactProteins = 0
        indexPhageProteins = 0

        while indexBactProteins < len(bactProteins):
            while indexPhageProteins < len(indexPhageProteins):
                score = self.calculateScoreBetweenTwoProt(bactProteins[indexBactProteins],phageProteins[indexPhageProteins])





    def calculateTotalScore(self):

        bacteries = self.getProteins()
        phages = self.getPhages()

        indexBacteries = 0
        indexPhages = 0

        while indexBacteries < len(bacteries):
            while indexPhages < len (phage):
                score = self.calculateScoreBetweenOneBacteryAndOnePhage(bacteries[indexBacteries],phages[indexPhages])



    def getProteins(self):
        #Recuperer les proteins




    def getPhages(self):
        #Recuperer phages



    def main(self):
        
        self.calculateTotalScore()