from app.algorithms.genetic.crossover import crossover
from app.algorithms.genetic.mutation import mutation_1, mutation_2
from app.algorithms.genetic.selection import *
from app.classes.graph import GraphMatrix
from app.classes.solution import Solution
from app.classes.vehicle import Vehicle
from app.utils.find_solution import find_solution
from app.utils.utils_functions import calc_vehicle_time
from app.classes.selection import ParentSelection, ChildrenSelection
from copy import deepcopy



def genetic_algorithm(graph: GraphMatrix, vehicles: list[Vehicle], number_of_iterations: int,
                      initial_population_size: int, population_size: int, parent_selection: ParentSelection, children_selection: ChildrenSelection,
                      stop_count: int, mutation: str, mutation_probability: int, max_parental_involvement: int)\
        -> list[Solution, list[int]]:
    """Algorytm genetyczny

    Args:
        graph (GraphMatrix): graf reprezentujący klinetów i zajezdnię
        vehicles (List[Vehicle]): lista pojazdów
        number_of_iterations (int): maksymalna liczba iteracji
        initial_population_size (int): rozmiar populacji początkowej
        population_size (int): rozmiar populacji w pętli algorytmu
        parent_selection (str): wybór pierwszej selekcji
        children_selection (str): wybór drugiej selekcji
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


    mutation_probability = min(mutation_probability / 100, 1)
    # TODO Wyrzucić po testowaniu
    ile_mutacji = 0

    stop_con = False
    best_solution = min(initial_population, key=lambda solution: solution.time)
    bests = []
    new_generation = deepcopy(initial_population)
    for _ in range(number_of_iterations):
        if stop_con:
            break
        last_generation = deepcopy(new_generation)
        parents = parent_selection_roulette(new_generation, population_size) if parent_selection == ParentSelection.Roulette \
            else parent_selection_tournament(initial_population, population_size)

        #Childrens to lista rozwiązań otrzymana po krzyżowaniu i mutacji
        childrens_crossover = crossover(parents)
        childrens_mutation = mutation_1(childrens_crossover, mutation_probability) if mutation == "1" else mutation_2(childrens_crossover, mutation_probability)

        # TODO Wyrzucić po testowaniu
        kasztan = [(children_cross, children_mut) for children_mut, children_cross in zip(childrens_mutation, childrens_crossover) if children_cross != children_mut]
        if len(kasztan) > 0:
            for child in kasztan:
                print(f"Przed: {child[0]}, procent mutacji {mutation_probability*100}")
                print(f"Po:    {child[1]} \n")
                ile_mutacji += 1


        childrens = [update_solution_time(solution, graph, solution.routes) for solution in childrens_mutation]

        new_generation = children_selection_ranking(last_generation, childrens, population_size, max_parental_involvement) if children_selection == ChildrenSelection.Ranking \
            else children_selection_roulette(last_generation, childrens, population_size, max_parental_involvement)


        #Sprawdzenie z ciekawości najlepszego rozwiązania samych losowo generowanych zbiorów i selekcji
        local_best = min(new_generation, key=lambda solution: solution.time)
        if local_best.time < best_solution.time:
            best_solution = local_best
        bests.append(local_best.time)

    # TODO Wyrzucić po testowaniu
    print(f"Tyle mutacji: {ile_mutacji}, procent mutacji {mutation_probability*100}")


    print(f"Best_solution: {best_solution}")
    return best_solution, bests


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


def update_solution_time(solution: Solution, graph: GraphMatrix, new_routes: dict[int:list[int]]) -> Solution:
    edges = {vehicle: [] for vehicle in solution.routes.keys()}
    times = {vehicle: 0 for vehicle in solution.routes.keys()}

    for idx, vehicle in enumerate(solution.routes.keys()):
        for i in range(1, len(new_routes[vehicle])):
            edges[vehicle].append(graph.matrix[new_routes[vehicle][i - 1]][new_routes[vehicle][i]])
        times[vehicle] = calc_vehicle_time(graph=graph, routes=new_routes[vehicle], edges=edges[vehicle])
    solution.calc_solution_time(times)
    return solution


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

