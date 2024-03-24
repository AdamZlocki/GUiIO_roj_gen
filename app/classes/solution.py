from typing import Dict, List

from app.classes.vehicle import Vehicle


class Solution:
    """Reprezentacja danego rozwiązania - routes to ścieżki przeybywane przez każdy z pojazdów, time to czas przypisany
    do danego rozwiązania"""
    def __init__(self, routes: Dict[Vehicle, List[int]], time: (float, int) = 0.0):
        self.routes = routes  # zakładając, że mamy więcej pojazdów niż 1 - kluczami w słowniku są id pojazdów,
        # a wartościami listy obsłużonych wierzchołków/pokonanych krawędzi
        self.time = time

    def __eq__(self, other):
        if self.time == other.time:
            if self.routes == other.routes:
                return True
            else:
                return False
        else:
            return False

    def __repr__(self):
        return f"{self.routes}, {self.time}"

    def __gt__(self, other):
        if self.time > other.time:
            return True
        else:
            return False

    def calc_solution_time(self, times):
        """wybiera czas rowiązania na podstawie czasów każdego z pojazdów"""
        self.time = max(times.values())
