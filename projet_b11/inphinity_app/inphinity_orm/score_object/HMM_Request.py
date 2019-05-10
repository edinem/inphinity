import requests

class HMM_request:
    """
    This class create requests to HMM API
    API doc : https://hmmer-web-docs.readthedocs.io/en/latest/api.html
    """
    def __init__(self):
        """
        Constructor of the HMM_request object.

        Define the host and the search
        """
        self.host = "https://www.ebi.ac.uk/Tools/hmmer/search/hmmscan"

    def hmm_search(self, seq, hmmdb="pfam"):
        """
        Search for domains in the sequence passed in parameter
        By default the hmmdb is pfam

        Return the list of domains

        :param seq: sequence of the protein
        :param hmmdb: database of the hmm search

        :type seq: text - required
        :type hmmdb: text - required

        """
        # Set the headers to send XML
        headers = {'Accept': 'application/json'}
        json_data = {'hmmdb': hmmdb, 'seq': seq}
        # Send the request
        r = requests.post(self.host, json=json_data, headers=headers)
        # recover json data
        data = r.json()
        result = []
        # foreach result, recover the PFAM id
        # Delete chars after . (?version of domain)
        for hits in data["results"]["hits"]:
            result.append(hits["acc"].split('.')[0])

        return result
