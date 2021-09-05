class Document:

    def __init__(self, address, size=0, norm=0):
        """
        :type address: str
        :type size: int
        :type norm: int
        """
        self.address = address
        self.size = size
        self.norm = norm
