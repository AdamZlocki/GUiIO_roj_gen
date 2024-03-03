class Vehicle:
    """Pojazd reprezentowany przez id i informuje o której może jechać do kolejnego wierzchołka"""
    def __init__(self, Id, free_at=0):
        self.Id = Id
        self.free_at = free_at

    def __eq__(self, other):
        if self.Id == other.Id:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.Id)

    def __repr__(self):
        return f"{self.Id}"

    def reset_free_at(self):
        self.free_at = 0