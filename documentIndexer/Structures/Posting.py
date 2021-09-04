class Posting:

    def __init__(self, doc_id, frequency, weight=0):
        """
        :type frequency: int
        :type weight: float
        """
        self.doc_id = doc_id
        self.frequency = frequency
        self.weight = weight
    def __str__(self):
        return f'Id documento = {self.doc_id} --- Frecuencia {self.frequency} ||'

