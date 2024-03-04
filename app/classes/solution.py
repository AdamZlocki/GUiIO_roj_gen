from typing import Dict, List

from app.classes.vehicle import Vehicle


class Solution:
    """Reprezentacja danego rozwiązania - routes to ścieżki przeybywane przez każdy z pojazdów, waiting_times to czas
    jaki każdy z pojazdów poświęca na oczekiwanie, time to czas przypisany do danego rozwiązania, LT to life time
    - charakterystyczne dla algorytmu pszczelego i niektórych innych więc nie wyrzucam na razie"""

    def __init__(self, routes: Dict[Vehicle, List[int]], waiting_times: Dict[Vehicle, Dict[int, float]],
                 time: (float, int) = 0.0, LT: int = 0):
        self.routes = routes  # zakładając że mamy więcej pojazdów niż 1 - kluczami w słowniku są id pojazdów,
        # a wartościami listy obsłużonych wierzchołków/pokonanych krawędzi
        self.time = time
        self.waiting_times = waiting_times
        self.LT = LT

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