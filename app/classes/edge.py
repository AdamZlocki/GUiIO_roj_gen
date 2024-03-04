class Edge:
    """Połączenie między wierzchołkami; reprezentuje czas przejazdu"""
    def __init__(self, start, end, time: float = 0):
        self.start = start
        self.end = end
        self.time = time

    def __eq__(self, other):
        if self.start == other.start and self.end == other.end:
            return True
        else:
            return False

    def __repr__(self):
        return f"({self.start} -- {self.time} --> {self.end})"
