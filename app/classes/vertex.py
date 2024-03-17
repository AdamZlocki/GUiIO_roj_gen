class Vertex:
    """Wierzchołek - reprezentowany przez id, informuje o swoim położeniu i czasie trwania serwisu"""
    def __init__(self, Id, x: (int, float), y: (int, float), service_time: (int, float),
                 is_base=False):
        if not is_base:
            self.Id = Id
            self.x = x
            self.y = y
            self.visited = 0
            self.service_time = service_time
        else:
            self.Id = Id
            self.x = x
            self.y = y
            self.visited = 1
            self.service_time = service_time

    def __eq__(self, other):
        if self.Id == other.Id:
            return True
        else:
            return False

    def __repr__(self):
        return f"{self.Id}"

    def __hash__(self):
        return hash(self.Id)
