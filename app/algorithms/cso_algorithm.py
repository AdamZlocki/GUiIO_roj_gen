from typing import Dict, List

from app.classes.vehicle import Vehicle
from app.utils.cso_functions import cso_step


def perform_swarm_movement(solution: Dict[Vehicle, List[int]], pi: Dict[Vehicle, List[int]]) -> Dict[Vehicle, List[int]]:
    """
    [Funkcja do usuniecia]
    Przeliczanie kazdego rozwiazania Xi i aktualizacja pg
    """
    return 0


def perform_dispersion(solution: Dict[Vehicle, List[int]], pg: Dict[Vehicle, List[int]]) -> Dict[Vehicle, List[int]]:
    """
    [Funkcja do usuniecia]
    Rozpraszanie i aktualizacja pg
    """
    return 0


def update_pg(solutions: List[Dict[Vehicle, List[int]]]) -> Dict[Vehicle, List[int]]:
    """
    Funkcja do aktualizacji pg
    """
    return 0


def calculate_pi(i, j) -> Dict[Vehicle, List[int]]:
    return 0


def cso_algorithm(max_step: int, visual, matrix_d, vehicles_number: int = 3, inner_w: int = 1) -> None:
    """
    A function implementing the Cockroach Swarm Optimization (CSO) algorithm.

    Attributes:
        max_step (int): The step size taken by the cockroach.
        visual (): The range of visibility for the cockroach.
        matrix_d (): The size of space D.
        vehicles_number (int): The number of vehicles
        inner_w (int): The inertia coefficient
    """
    t_max = 50
    end_condition = False
    # 1 - Population generation, population evaluation -> Prawdopodobnie poza algo
    vehicles = [Vehicle(Id=i) for i in range(1, vehicles_number+1)]
    sol1 = {vehicles[0]: [2, 5], vehicles[1]: [9, 3, 8, 7], vehicles[2]: [4, 1, 6]}
    sol2 = {vehicles[0]: [9, 8, 5, 1, 2], vehicles[1]: [4, 3], vehicles[2]: [7, 6]}
    solutions = [sol1, sol2]
    for _ in range(t_max):
        # 2 - Find pi and pg
        pg = solutions[0]   # TODO: Change the method of calculating pg.
        for sol_i in range(len(solutions)):
            p_list = []
            for sol_j in range(len(solutions)):
                if sol_i != sol_j:
                    p_list.append(calculate_pi(solutions, sol_j))
            pi = p_list[0]  # TODO: Change the method of calculating pi
            # 3 - Implementation of swarm movement and updating pg
            if pi is not None:
                cso_step(solutions[sol_i], pi, vehicles)
                pg = update_pg(solutions)
            # 4 - Implementation of dispersion and updating pg
            solutions[sol_i] = perform_dispersion(solutions[sol_i], pg)
            pg = update_pg(solutions)
            if end_condition:   # TODO: Implement algorithm's termination condition.
                return None
