from Posting import Posting


class Term:

    def __init__(self, term, frequency):
        """
        :type frequency: int
        :type term: str
        """
        self.term = term
        self.frequency = frequency
        self.inv_frequency_vec = 0
        self.inv_frequency_bm5 = 0
        self.postings = {}

    def insert_posting(self, doc_id):
        if doc_id in self.postings.keys():
            self.postings[doc_id].frequency += 1
        else:
            self.postings[doc_id] = Posting(doc_id, 1)

    def __str__(self):
        string = f'Término {self.term} ------ Frecuencia {self.frequency} \n'
        for key in self.postings.keys():
            string += str(self.postings[key])
        return string + "\n \n ================ \n"
