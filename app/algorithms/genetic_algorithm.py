# from typing import List

from app.classes.graph import GraphMatrix
from app.classes.solution import Solution
from app.classes.vehicle import Vehicle
from app.utils.find_solution import find_solution
from app.utils.utils_functions import calc_vehicle_time, calc_solution_time
from copy import deepcopy


def genetic_algorithm(graph: GraphMatrix, vehicles: list[Vehicle], number_of_iterations: int,
                      initial_population_size: int, population_size: int, first_selection: str, second_selection: str,
                      stop_count: int, mutation: str, mutation_probability: int, max_parental_involvement: int)\
        -> list[Solution, list[Solution]]:
    """Algorytm genetyczny

    Args:
        graph (GraphMatrix): graf reprezentujący klinetów i zajezdnię
        vehicles (List[Vehicle]): lista pojazdów
        number_of_iterations (int): maksymalna liczba iteracji
        initial_population_size (int): rozmiar populacji początkowej
        population_size (int): rozmiar populacji w pętli algorytmu
        first_selection (str): wybór pierwszej selekcji
        second_selection (str): wybór drugiej selekcji
        stop_count (int): warunek stopu działania algorytmu po liczbie iteracji bez poprawy rozwiązania
        mutation (str): wybór mutacji 
        mutation_probability (int): prawdopodobieństwo zajścia mutacji dla każdego osobnika
        max_parental_involvement (int): maksymalny udział rodziców w kolejnym pokoleniu
    """
    # 1. Inicjalizacja populacji początkowej
    # 2. Główna pętla algorytmu:
    #   1. Sprawdzenie warunku stopu
    #   2. Selekcja par osobników do procesu krzyżowania 
    #   3. Operacja krzyżowania dla wyselekcjonowanych par
    #   4. Operacja mutacji dla nowej populacji
    #   5. Wyselekcjonowanie populacji dla kolejnej iteracji
    #   6. Zapamiętanie aktualnie najlepszego i dodanie go do listy najlepszych
    # print(graph.matrix[0][1].time)

    initial_population = create_initial_population(solutions=[], graph=graph, vehicles=vehicles,
                                                   size_of_initial_population=initial_population_size)

    # przykładowe użycie funkcji create_new_solution() dla crossover i mutacji - dla crossover powstaje nowe
    # rozwiązanie, a dla mutacji aktualne rozwiązanie się zmienia - dla mutacji nie trzeba nic robić; dla krzyżowania
    # wystarczy dodawać nowe rozwiąznia do populacji
    print(f"initial:       {initial_population[0]}")
    new_routes = {1: [0, 1, 5, 12, 7, 15, 0], 2: [0, 13, 6, 11, 14, 10, 0], 3: [0, 4, 2, 8, 3, 16, 9, 0]}
    new_sol = create_new_solution(initial_population[0], new_routes, 'cross', graph)
    print(f"new_sol:       {new_sol}\ninitial after: {initial_population[0]}\n")
    print(f"initial:       {initial_population[0]}")
    new_routes = {1: [0, 1, 5, 12, 7, 15, 0], 2: [0, 13, 6, 11, 14, 10, 0], 3: [0, 4, 2, 8, 3, 16, 9, 0]}
    new_sol = create_new_solution(initial_population[0], new_routes, 'mut', graph)
    print(f"new_sol:       {new_sol}\ninitial after: {initial_population[0]}\n")

    return 0, [0]


def create_new_solution(solution: Solution, routes: dict[int:list[int]], operator: str, graph: GraphMatrix) -> Solution:
    if operator == 'mut':
        for vehicle, new_route in zip(solution.routes.keys(), routes.values()):
            solution.routes[vehicle] = new_route
        update_solution_time(solution, graph, routes)
        return solution

    elif operator == 'cross':
        new_solution = deepcopy(solution)
        for vehicle, new_route in zip(solution.routes.keys(), routes.values()):
            new_solution.routes[vehicle] = new_route
        update_solution_time(new_solution, graph, routes)
        return new_solution


def update_solution_time(solution: Solution, graph: GraphMatrix, new_routes: dict[int:list[int]]) -> None:
    edges = {vehicle: [] for vehicle in solution.routes.keys()}
    times = {vehicle: 0 for vehicle in solution.routes.keys()}

    for idx, vehicle in enumerate(solution.routes.keys()):
        for i in range(1, len(new_routes[vehicle.Id])):
            edges[vehicle].append(graph.matrix[new_routes[vehicle.Id][i - 1]][new_routes[vehicle.Id][i]])
        times[vehicle] = calc_vehicle_time(graph=graph, routes=new_routes[vehicle.Id], edges=edges[vehicle])
    time = calc_solution_time(times)
    solution.time = time


# Wzięte z `bee_algorithm.py`
def create_initial_population(solutions, graph, vehicles, size_of_initial_population) -> list[Solution]:
    while len(solutions) < size_of_initial_population:  # utworzenie zadanej ilości początkowych rozwiązań
        sol = find_solution(graph=graph, vehicles=vehicles)
        if sol not in solutions:
            solutions.append(sol)
    return solutions


# Wzięte z `bee_algorithm.py`, raczej się przyda
def sort_solutions(solutions, size_of_iteration, best):
    solutions_sorted = []  # posortowanie rozwiązań
    while len(solutions_sorted) < size_of_iteration:
        solutions_sorted.append(solutions.pop(solutions.index(min(solutions))))
    if not best:
        best = solutions_sorted[0]
    else:
        if solutions_sorted[0] < best:
            best = solutions_sorted[0]
    return solutions_sorted.copy(), best


def first_selection_1(population: list[Solution], population_size: int) -> list[(Solution, Solution)]:
    """ Ruletki
    """
    return []


def first_selection_2(population: list[Solution], population_size: int) -> list[(Solution, Solution)]:
    """ Rankingowa/Turniejowa
    """
    return []


def second_selection_1(population: list[Solution], population_size: int, max_parental_involvement: int) -> list[Solution]:
    """ Rankingowa

    Returns:
        list[Solution]: _description_
    """
    return []


def second_selection_2(population: list[Solution], population_size: int, max_parental_involvement: int) -> list[Solution]:
    """ Ruletki/Turniejowa

    Returns:
        list[Solution]: _description_
    """
    return []


def crossover(population: list[(Solution, Solution)]) -> list[Solution]:
    return []


def mutation_1(population: list[Solution]) -> list[Solution]:
    return []


def mutation_2(population: list[Solution]) -> list[Solution]:
    return []
