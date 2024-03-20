
# from typing import List

from classes.graph import GraphMatrix
from classes.solution import Solution
from classes.vehicle import Vehicle
from utils.find_solution import find_solution
from utils.utils_functions import calc_vehicle_time, calc_solution_time


def genetic_algorithm(graph: GraphMatrix, vehicles: list[Vehicle], number_of_iterations: int, initial_population_size: int,
                      population_size: int, first_selection: str, second_selection: str, stop_count: int, mutation: str,
                      mutation_probability: int, max_parental_involvement: int) -> list[Solution, list[Solution]]:
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

    return "best, bests"

def create_new_solution(solution: Solution, route: list[int], operator: str) -> Solution:
    # jeśli mutacja to: solution.routes = route i solution.time = calc_vehicle_time()
    # jeśli krzyżowanie to kopia i to co wyżej
    return 0

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
    return 0

def first_selection_2(population: list[Solution], population_size: int) -> list[(Solution, Solution)]:
    """ Rankingowa/Turniejowa
    """
    return 0

def second_selection_1(population: list[Solution], population_size: int, max_parental_involvement: int) -> list[Solution]:
    """ Rankingowa

    Returns:
        list[Solution]: _description_
    """
    return 0

def second_selection_2(population: list[Solution], population_size: int, max_parental_involvement: int) -> list[Solution]:
    """ Ruletki/Turniejowa

    Returns:
        list[Solution]: _description_
    """
    return 0

def crossover(population: list[(Solution, Solution)]) -> list[Solution]:
    return 0

def mutation_1(population: list[Solution]) -> list[Solution]:
    return 0

def mutation_2(population: list[Solution]) -> list[Solution]:
    return 0