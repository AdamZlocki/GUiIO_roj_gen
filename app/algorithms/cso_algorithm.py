from typing import Dict, List

from app.classes.vehicle import Vehicle
from app.utils.cso_functions import cso_step

from bee_algorithm import *
from app.utils.cso_functions import *

# def perform_swarm_movement(solution: Dict[Vehicle, List[int]], pi: Dict[Vehicle, List[int]]) -> Dict[Vehicle, List[int]]:
#     """
#     [Funkcja do usuniecia]
#     Przeliczanie kazdego rozwiazania Xi i aktualizacja pg
#     """
#     return 0


# def perform_dispersion(solution: Dict[Vehicle, List[int]], pg: Dict[Vehicle, List[int]]) -> Dict[Vehicle, List[int]]:
#     """
#     [Funkcja do usuniecia]
#     Rozpraszanie i aktualizacja pg
#     """
#     return 0


# def update_pg(solutions: List[Dict[Vehicle, List[int]]]) -> Dict[Vehicle, List[int]]:
#     """
#     Funkcja do aktualizacji pg
#     """
#     return 0


# def calculate_pi(i, j) -> Dict[Vehicle, List[int]]:
#     return 0



def cso_algorithm(graph: GraphMatrix, vehicles: List[Vehicle], visual, 
                  num_of_iterations: int = 50, size_of_iteration: int = 10, max_step: int = 1,
                  vehicles_number: int = 3, inner_w: int = 1) -> None:
    """
    A function implementing the Cockroach Swarm Optimization (CSO) algorithm.

    Attributes:
        max_step (int): The step size taken by the cockroach.
        visual (): The range of visibility for the cockroach.
        graph: The size of space D.
        vehicles_number (int): The number of vehicles
        inner_w (int): The inertia coefficient
    """
    end_condition = False

    # 1 - Population generation, population evaluation -> Prawdopodobnie poza algo
    # vehicles = [Vehicle(Id=i) for i in range(1, vehicles_number+1)]
    # sol1 = {vehicles[0]: [2, 5], vehicles[1]: [9, 3, 8, 7], vehicles[2]: [4, 1, 6]}
    # sol2 = {vehicles[0]: [9, 8, 5, 1, 2], vehicles[1]: [4, 3], vehicles[2]: [7, 6]}
    # solutions = [sol1, sol2]

    # utworzenie zadanej ilości początkowych rozwiązań
    solutions = create_initial_solutions([], graph, vehicles, size_of_iteration=size_of_iteration)
    
    # posortowanie rozwiązań i zapamiętanie najlepszego
    solutions, pg = sort_solutions(solutions, size_of_iteration=size_of_iteration, best=0) 
    N = len(solutions)

    for _ in range(num_of_iterations):
        # 2 - Find pi and pg
        # pg = solutions[0]   # TODO: Change the method of calculating pg.
        pg_list = []
        for sol_i in range(N):
            # p_list = []
            for sol_j in range(N):
                if cso_get_step_distance(solutions[sol_j], solutions[sol_i], vehicles) < visual and solutions[sol_j].time < solutions[sol_i].time:
                    # p_list.append(calculate_pi(solutions, sol_j))
                    pi = solutions[sol_j]

            # Sprawdzić czy pi istnieje
                    
            # pi = p_list[0]  # TODO: Change the method of calculating pi
            
            # 3 - Implementation of swarm movement and updating pg
            if pi is not None:
                solutions[sol_i] = cso_step(solutions[sol_i], pi, vehicles)
                solutions, pg = sort_solutions(solutions, size_of_iteration=size_of_iteration, best=pg)

            # 4 - Implementation of dispersion and updating pg
            solutions[sol_i] = dispersal(0.5, solutions[sol_i], vehicles)
            solutions, pg = sort_solutions(solutions, size_of_iteration=size_of_iteration, best=pg)
            pg_list.append(pg)
            # if end_condition:   # TODO: Implement algorithm's termination condition.
            #     return None

        #####
        # K - czy się nie gryzie z dispersal
        ####
    list_of_sols, xk = sort_solutions(solutions, size_of_iteration=50, best=pg)
    return list_of_sols, xk