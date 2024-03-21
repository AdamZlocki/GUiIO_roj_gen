from typing import Dict, List

from app.classes.vehicle import Vehicle


class Solution:
    """Reprezentacja danego rozwiązania - routes to ścieżki przeybywane przez każdy z pojazdów, time to czas przypisany
    do danego rozwiązania, LT to life time - charakterystyczne dla algorytmu pszczelego i niektórych innych więc nie
    wyrzucam na razie"""

    def __init__(self, routes: Dict[Vehicle, List[int]], time: (float, int) = 0.0): # LT: int = 0
        self.routes = routes  # zakładając że mamy więcej pojazdów niż 1 - kluczami w słowniku są id pojazdów,
        # a wartościami listy obsłużonych wierzchołków/pokonanych krawędzi
        self.time = time
        # self.LT = LT to już nie potrzebne, nie ma czasu życia obiektu

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