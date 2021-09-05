class Posting:

    def __init__(self, doc_id, frequency):
        """
        :type frequency: int
        :type weight: float
        """
        self.doc_id = doc_id
        self.frequency = frequency
        self.weight_vec = 0
        self.weight_bm25 = 0

    def __str__(self):
        return f'Id documento = {self.doc_id} --- Frecuencia {self.frequency} ||'
