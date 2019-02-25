import json
from rest_client.GetRest import GetRest
from rest_client.PostRest import PostRest

class ContigAPI(object):
    """
    This class manage the requests for the Contig objects into the restAPI

    :param function: the name of the function to access in the rest API
    :type function: string
    """

    def __init__(self, function='contig/'):
        """
        Initialization of the class

        :param function: name of the function

        :type function: string (url)

        """
        self.function = function

    def get_all(self):
        """
        get all the Contigs on the database

        :return: json file with all the data
        :rtype: string (json format)
        """
        result_get = GetRest(function = self.function).performRequest()
        return result_get

    def set_contig(self, jsonData):
        """
        set new contig in the database

        :return: json file with the last contig created
        :rtype: string (json format)
        """
        jsonData = json.dumps(jsonData)
        result_post = PostRest(function = self.function, dataDict = jsonData).performRequest()
        return result_post

    def getByOrganismID(self, organism_id):
        """
        get all contigs of a given organism

        :param organism_id: organism ID

        :type organism_id: int

        :return: all the contigs of the given organism id
        :rtype: ProteinJson
        """

        self.function += 'organism_id/' + str(organism_id)

        result_get = GetRest(function = self.function).performRequest()
        return result_get