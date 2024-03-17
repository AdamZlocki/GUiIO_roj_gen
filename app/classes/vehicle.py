class Vehicle:
    """Pojazd reprezentowany przez id i informuje o której może jechać do kolejnego wierzchołka"""
    def __init__(self, Id):
        self.Id = Id

    def __eq__(self, other):
        if self.Id == other.Id:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.Id)

    def __repr__(self):
        return f"{self.Id}"
