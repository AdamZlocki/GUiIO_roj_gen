from random import shuffle, sample
from typing import List, Dict

from app.classes.edge import Edge
from app.classes.graph import GraphMatrix
from app.classes.solution import Solution
from app.classes.vehicle import Vehicle
from app.utils.utils_functions import calc_vehicle_time


def find_solution(graph: GraphMatrix, vehicles: List[Vehicle]):
    """Funkcja do znajdowania losowego rozwiązania w przestrzeni rozwiązań"""
    routes, edges, times = initialize_data(vehicles)
    num_of_vehicles = len(vehicles)

    randomized_vertex_list = [idx for idx in range(1, len(graph.matrix[0]))]  # wymieszanie wszystkich wierzchołków
    shuffle(randomized_vertex_list)

    # stworzenie listy indeksów, w których będziemy dzielić listę wymieszanych wierzchołkow
    cut_idx = sample(range(1, max(randomized_vertex_list)), num_of_vehicles - 1)
    cut_idx.sort()

    for idx, vehicle in enumerate(vehicles):
        # pocięcie listy wierzchołków na ścieżki dla każdego pojazdu
        if idx == 0:
            routes[vehicle] += randomized_vertex_list[:cut_idx[idx]]
            routes[vehicle].append(0)
        elif idx == num_of_vehicles - 1:
            routes[vehicle] += randomized_vertex_list[cut_idx[idx - 1]:]
            routes[vehicle].append(0)
        else:
            routes[vehicle] += randomized_vertex_list[cut_idx[idx - 1]:cut_idx[idx]]
            routes[vehicle].append(0)

        #  uzupełnienie listy krawędzi dla każdego pojazdu
        for i in range(1, len(routes[vehicle])):
            edges[vehicle].append(graph.matrix[routes[vehicle][i - 1]][routes[vehicle][i]])
        #  obliczenie czasu podróży dla każdego pojadzu
        times[vehicle] = calc_vehicle_time(graph=graph, routes=routes[vehicle], edges=edges[vehicle])

    solution = Solution(routes=routes)
    solution.calc_solution_time(times=times)  # obliczenie czasu rozwiązania

    for vertex in graph.list[1:]:  # reset grafu
        vertex.visited = 0

    return solution


def initialize_data(vehicles):
    routes: Dict[Vehicle, List[int]] = {}
    edges: Dict[Vehicle, List[Edge]] = {}
    times: Dict[Vehicle, float] = {}

    for vehicle in vehicles:
        routes[vehicle] = [0]
        edges[vehicle] = []
        times[vehicle] = 0

    return routes, edges, times


# def select_neighbour(current, graph, vehicle):
#     neighbours = graph.neighbours(current)  # wyszukanie sąsiadów i usunięcie wierzchołka Bazy
#     if 0 in neighbours:
#         neighbours.remove(0)
#
#     neighbours_to_delete = []  # wyszukanie już odwiedzonych sąsiadów lub sąsiadów z niepasującym oknem
#     # czasowym
#     for neigh in neighbours:
#         edge_time = graph.matrix[current][neigh].time
#         neigh_vertex = graph.get_vertex(neigh)
#         time_at_place = vehicle.free_at + edge_time
#         if neigh_vertex.visited == 1 or time_at_place >= neigh_vertex.time_window[1]:
#             neighbours_to_delete.append(neigh)
#
#     for neigh in neighbours_to_delete:  # usunięcie niedozwolonych sąsiadów
#         neighbours.remove(neigh)
#
#     if len(neighbours):  # jeśli zostali jeszcze jacyś sąsiedzi wylosowanie nastepnego wierzchołka
#         neighbour = choice(neighbours)
#         neigh_vertex = graph.get_vertex(neighbour)
#         edge_time = graph.matrix[current][neighbour].time
#         time_at_place = vehicle.free_at + edge_time
#         # sprawdzenie czy pojazd nie przyjedzie przed rozpoczęciem okna czasowego
#         if time_at_place < neigh_vertex.time_window[0]:
#             waiting_times[vehicle][neighbour] = neigh_vertex.time_window[0] - time_at_place
#         else:
#             waiting_times[vehicle][neighbour] = 0
#         graph.get_vertex(neighbour).visited = 1
#         vehicle.free_at += edge_time + neigh_vertex.service_time + waiting_times[vehicle][neighbour]
#     else:  # jeśli nie -> wybranie 0 i powrót do bazy
#         neighbour = 0
#
#     return neighbour


# def reset_data(graph, vehicles, routes, edges, times):
#     graph.reset_visited()
#     for vehicle in vehicles:
#         routes[vehicle] = [0]
#         edges[vehicle] = []
#         times[vehicle] = 0
#         vehicle.reset_free_at()
