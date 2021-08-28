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
