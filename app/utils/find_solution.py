from random import choice
from typing import List, Dict

from app.classes.edge import Edge
from app.classes.graph import GraphMatrix
from app.classes.solution import Solution
from app.classes.vehicle import Vehicle
from app.utils.utils_functions import all_visited, calc_solution_time, calc_vehicle_time


def find_solution(graph: GraphMatrix, vehicles: List[Vehicle]):
    """Funkcja do znajdowania losowego rozwiązania w przestrzeni rozwiązań przy założeniu że jest ono dopuszczalane"""
    routes, edges, currents, times, waiting_times = initialize_data(vehicles)

    while not all_visited(graph):  # pętla wykonywana dopóki nie wszystkie wierzchołki są odwiedzone
        old_currents = currents.copy()
        for vehicle in vehicles:
            if not (currents[vehicle] == 0 and len(routes[vehicle]) > 1):
                # jeśli trasa jest dłuższa niż 1 wierzchołek i na końcu jest 0 to znaczy że trasa dla tego pojazdu jest już skończona

                current = currents[vehicle]
                neighbour = select_neighbour(current, graph, vehicle, waiting_times)
                edges[vehicle].append(graph.matrix[current][neighbour])  # aktualizacja tablic dla danego pojazdu
                routes[vehicle].append(neighbour)
                currents[vehicle] = neighbour

        if old_currents == currents:  # jeśli nie dodano żadnego nowego punktu na trasach -> reset słowników, czasów
            # pojazdów i odwiedzenia wierzchołków
            reset_data(graph, vehicles, routes, edges, currents, times, waiting_times)

    for vehicle in vehicles:
        if routes[vehicle][-1] != 0:
            routes[vehicle].append(0)
            edges[vehicle].append(graph.matrix[currents[vehicle]][0])
            currents[vehicle] = 0
        times[vehicle] = calc_vehicle_time(graph=graph, routes=routes[vehicle], edges=edges[vehicle],
                                           waiting_times=waiting_times[vehicle])

    time = calc_solution_time(times)

    solution = Solution(routes=routes, time=time, waiting_times=waiting_times)

    for vertex in graph.list[1:]:  # reset grafu i pojazdów
        vertex.visited = 0
    for vehicle in vehicles:
        vehicle.reset_free_at()

    return solution

def initialize_data(vehicles):
    routes: Dict[Vehicle, List[int]] = {}
    edges: Dict[Vehicle, List[Edge]] = {}
    currents: Dict[Vehicle, int] = {}
    times: Dict[Vehicle, float] = {}
    waiting_times: Dict[Vehicle, Dict[int, float]] = {}

    for vehicle in vehicles:
        routes[vehicle] = [0]
        edges[vehicle] = []
        currents[vehicle] = 0
        times[vehicle] = 0
        waiting_times[vehicle] = {}

    return routes, edges, currents, times, waiting_times
def select_neighbour(current, graph, vehicle, waiting_times):
    neighbours = graph.neighbours(current)  # wyszukanie sąsiadów i usunięcie wierzchołka Bazy
    if 0 in neighbours:
        neighbours.remove(0)

    neighbours_to_delete = []  # wyszukanie już odwiedzonych sąsiadów lub sąsiadów z niepasującym oknem
    # czasowym
    for neigh in neighbours:
        edge_time = graph.matrix[current][neigh].time
        neigh_vertex = graph.get_vertex(neigh)
        time_at_place = vehicle.free_at + edge_time
        if neigh_vertex.visited == 1 or time_at_place >= neigh_vertex.time_window[1]:
            neighbours_to_delete.append(neigh)

    for neigh in neighbours_to_delete:  # usunięcie niedozwolonych sąsiadów
        neighbours.remove(neigh)

    if len(neighbours):  # jeśli zostali jeszcze jacyś sąsiedzi wylosowanie nastepnego wierzchołka
        neighbour = choice(neighbours)
        neigh_vertex = graph.get_vertex(neighbour)
        edge_time = graph.matrix[current][neighbour].time
        time_at_place = vehicle.free_at + edge_time
        # sprawdzenie czy pojazd nie przyjedzie przed rozpoczęciem okna czasowego
        if time_at_place < neigh_vertex.time_window[0]:
            waiting_times[vehicle][neighbour] = neigh_vertex.time_window[0] - time_at_place
        else:
            waiting_times[vehicle][neighbour] = 0
        graph.get_vertex(neighbour).visited = 1
        vehicle.free_at += edge_time + neigh_vertex.service_time + waiting_times[vehicle][neighbour]
    else:  # jeśli nie -> wybranie 0 i powrót do bazy
        neighbour = 0

    return neighbour

def reset_data(graph, vehicles, routes, edges, currents, times, waiting_times):
    graph.reset_visited()
    for vehicle in vehicles:
        routes[vehicle] = [0]
        edges[vehicle] = []
        currents[vehicle] = 0
        times[vehicle] = 0
        waiting_times[vehicle] = {}
        vehicle.reset_free_at()