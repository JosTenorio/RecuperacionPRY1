
from Term import Term
class Collection:

    def __init__(self, address, stopwords):
        """
        :type address: str
        :type stopwords: list
        """
        self.address = address
        self.size = 0
        self.stopwords = stopwords
        self.avr_length = 0
        self.dictionary = {}
        self.documents = {}
    def insert_term(self,word,doc_id):
        if word in self.dictionary.keys():
            self.dictionary[word].frequency += 1
            self.dictionary[word].insert_posting(doc_id)
        else:
            term = Term(word,1)
            term.insert_posting(doc_id)
            self.dictionary[word] = term
    def __str__(self):
        string = ""
        for key in self.dictionary.keys():
            string+=(str(self.dictionary[key]))
        return string
