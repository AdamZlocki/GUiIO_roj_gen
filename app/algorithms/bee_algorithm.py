from typing import List

from app.classes.graph import GraphMatrix
from app.classes.solution import Solution
from app.classes.vehicle import Vehicle
from app.utils.find_solution import find_solution
from app.utils.neigbourhood import neighbourhood


def bee_algorythm(graph: GraphMatrix, vehicles: List[Vehicle], num_of_iterations: int = 10, size_of_iteration: int = 10,
                  num_of_elite: int = 2, num_of_bests: int = 3, size_of_neighbourhood_elite: int = 10,
                  size_of_neighbourhood_best: int = 5, max_LT: int = 3, switch_in_all_routes=False):
    """
    :param graph: graf reprezentujący klinetów i zajezdnię
    :param vehicles: lista pojazdów
    :param num_of_iterations: liczba iteracji
    :param size_of_iteration: liczba rozwiązań rozważanych w danej iteracji
    :param num_of_elite: liczba rozwiązań elitarnych
    :param num_of_bests: liczba rozwiązań najlepszych (gorsze)
    :param size_of_neighbourhood_elite: rozmiar sąsiedztwa rozwiązań elitarnych
    :param size_of_neighbourhood_best: rozmiar sąsiedztwa rozwiązań najlepszych
    :param max_LT: maksymalny czas życia rozwiązania
    :param switch_in_all_routes: wybór czy przy szukaniu sąsiadów zmieniamy ścieżkę dla jednego pojazdu (False) czy
                                 wszystkich (True)
    :return: best - najlepsze rozwiązanie; bests - lista kosztów najlepszych rozwiązań po danej iteracji
    """
    solutions = []
    counter_of_iterations = 0
    bests = []
    best: (Solution, int) = 0
    while counter_of_iterations < num_of_iterations:  # dopóki nie wykonano oczekiwanej liczby iteracji powtarzamy

        if not check_continuation(bests):  # jeśli nie było poprawy przerywamy algorytm
            break

        if solutions:  # w przypadku gdy coś znajduje się w liście rozwiązań - usunięcie rozwiązń, które przekroczyły
            # maksymalną długość życia
            solutions = remove_expired_solutions(solutions, max_LT)

        solutions = create_initial_solutions(solutions, graph, vehicles, size_of_iteration) # utworzenie zadanej ilości początkowych rozwiązań
        solutions, best = sort_solutions(solutions, size_of_iteration, best) #posortowanie rozwiązań i zapamiętanie najlepszego



        elite_solutions = solutions[:num_of_elite] # utworzenie listy rozwiązań elitarnych
        best_solutions = solutions[num_of_elite:num_of_elite + num_of_bests] # utworzenie listy rozwiązań najlepszych (gorsze od elitarych)

        elite_solutions = generate_neighbourhood(elite_solutions, graph, size_of_neighbourhood_elite, switch_in_all_routes)
        best_solutions = generate_neighbourhood(best_solutions, graph, size_of_neighbourhood_best, switch_in_all_routes)

        solutions = elite_solutions + best_solutions
        solutions, best = sort_solutions(solutions, num_of_bests + num_of_elite, best) # posortowanie rozwiązań i zapamiętanie najlepszego

        for solution in solutions:
            solution.LT += 1

        counter_of_iterations += 1
        bests.append(best.time)

        # print(counter_of_iterations)
    return best, bests

def check_continuation(bests):
    return len(bests) <= 15 or abs(bests[-1] - bests[-15]) > 5

def remove_expired_solutions(solutions, max_LT):
    # w przypadku gdy coś znajduje się w liście rozwiązań - usunięcie rozwiązń, które przekroczyły
    # maksymalną długość życia
    for solution in solutions:
        if solution.LT > max_LT:
            solutions.remove(solution)
    return solutions
    
def create_initial_solutions(solutions, graph, vehicles, size_of_iteration):
    while len(solutions) < size_of_iteration:  # utworzenie zadanej ilości początkowych rozwiązań
        sol = find_solution(graph=graph, vehicles=vehicles)
        if sol not in solutions:
            solutions.append(sol)
    return solutions

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

def generate_neighbourhood(solutions, graph, size, switch_in_all_routes):
    for solution in solutions:  # utworzenie sąsiedztwa rozwiązań i ewentualne zastąpienie ich ich
        # najlepszymi sąsiadami
        solution.neighbourhood = []
        solution.neighbourhood = neighbourhood(graph=graph, solution=solution, size=size,
                                               switch_in_all_routes=switch_in_all_routes)
        best_neighbour = solution.neighbourhood[solution.neighbourhood.index(min(solution.neighbourhood))]
        if best_neighbour < solution:
            solutions[solutions.index(solution)] = best_neighbour
    return solutions