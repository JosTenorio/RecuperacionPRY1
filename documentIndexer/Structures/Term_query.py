class Term_query:

    def __init__(self, term, frequency, weight):
        """
        :type frequency: int
        :type term: str
        """
        self.term = term
        self.frequency = frequency
        self.weight = weight

    def __str__(self):
        return (f"Termino {self.term} | Frecuencia {self.frequency} | Peso {self.weight} ")
