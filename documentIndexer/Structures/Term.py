class Term:

    def __init__(self, frequency, inv_frequency):
        """
        :type frequency: int
        :type inv_frequency: float
        """
        self.frequency = frequency
        self.inv_frequency = inv_frequency
        self.postings = {}