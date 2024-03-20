import time

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from classes.edge import Edge
from classes.graph import GraphMatrix
from classes.vehicle import Vehicle
from classes.vertex import Vertex

path_date = r"./dane/Dane_VRP_WT_ST.xlsx"


def calc_solution_time(times: dict) -> int:
    """wybiera czas rowiązania na podstawie czasów każdego z pojazdów"""
    return max(times.values())


def calc_vehicle_time(graph: GraphMatrix, routes, edges) -> float:
    """czas = suma czasów serwisu + łączny czas oczekiwania + łączny czas krawędzi (wszystko dla danego pojazdu)"""
    service_times = []
    for vertex_idx in routes:
        vertex = graph.get_vertex(vertex_idx=vertex_idx)
        service_times.append(vertex.service_time)
    time = sum(service_times)
    for edge in edges:
        time += edge.time
    return round(time, 2)


# def is_matrix_square(matrix):
#     N = len(matrix)
#     for row in range(N):
#         if len(matrix[row]) != N:
#             return False
#     return True
#
#
# def is_matrix_symetrical(matrix):
#     N = len(matrix)
#     for i in range(N):
#         for j in range(N):
#             if matrix[i][j] != matrix[j][i]:
#                 return False
#     return True
#
#
# def has_matrix_0_diagonal(matrix):
#     N = len(matrix)
#     for i in range(N):
#         if matrix[i][i] != '0':
#             return False
#     return True


def all_visited(graph: GraphMatrix):
    """sprawdzenie czy wszystkie wierzchołki w grafie zostały odwiedzone"""
    result = True
    for vertex in graph.list:
        if vertex.visited == 0:
            result = False
            break
    return result


def calculate_edge_time(vertex1: Vertex, vertex2: Vertex):
    """zakładamy prędkość 1 kilometr na minutę -> czas [min] = dystans [km]"""
    return round(np.sqrt((vertex2.x - vertex1.x) ** 2 + (vertex2.y - vertex1.y) ** 2), 2)


def excel_to_graph(path: str, sheet_name: str):
    """czas serwisowania i okna czasowe są w minutach; x i y w kilometrach"""
    data = pd.read_excel(path, sheet_name=sheet_name)
    depot = data.iloc[0, :]
    clients = data.iloc[1:, :]
    graph = GraphMatrix()
    graph.insert_vertex(
        Vertex(Id=depot['StringID'], x=depot['x'], y=depot['y'], service_time=depot['ServiceTime'], is_base=True))

    for client_idx in range(clients.shape[0]):
        client = clients.iloc[client_idx]
        graph.insert_vertex(Vertex(Id=client['StringID'], x=client['x'], y=client['y'],
                                   service_time=client['ServiceTime']))

    for idx, vertex in enumerate(graph.list):
        for idx2, vertex2 in enumerate(graph.list[idx + 1:]):
            real_idx2 = idx2 + idx + 1
            edge_time = calculate_edge_time(vertex1=vertex, vertex2=vertex2)
            graph.insert_edge(vertex1_idx=idx, vertex2_idx=real_idx2,
                              edge=Edge(start=vertex, end=vertex2, time=edge_time))
            graph.insert_edge(vertex1_idx=real_idx2, vertex2_idx=idx,
                              edge=Edge(start=vertex2, end=vertex, time=edge_time))

    return graph


def plot_results(sheet_name: str, num_of_vehicles: int, algorithm: str, num_of_runs: int = 20,
                 switch_in_all_routes=False):
    graph = excel_to_graph(path=path_date,
                           sheet_name=sheet_name)

    vehicles = []
    for i in range(1, num_of_vehicles + 1):
        vehicles.append(Vehicle(Id=i))

    multiple_bests = []
    times_measured = []

    while len(multiple_bests) < num_of_runs:
        start_time, end_time = 0, 0
        bests = []
        if algorithm == 'bee':
            from app.algorithms import bee_algorithm

            start_time = time.time()
            sol, bests = bee_algorithm.bee_algorythm(graph=graph, vehicles=vehicles, num_of_iterations=100,
                                                     size_of_iteration=20, num_of_elite=3, num_of_bests=5,
                                                     size_of_neighbourhood_elite=5,
                                                     size_of_neighbourhood_best=3, max_LT=2,
                                                     switch_in_all_routes=switch_in_all_routes)
            end_time = time.time()

        times_measured.append(end_time - start_time)
        multiple_bests.append(bests)
        print(len(multiple_bests))
        graph.reset_visited()

    # print(f"Średni czas pracy algorytmu: {np.mean(times_measured)}")

    for bests in multiple_bests:  # w każdym uruchomieniu algorytm może skończyć się w różnej liczbie iteracji więc
        # w celu poprawnego wyroswania średniej trzeba dorównać ilość iteracji do tej największej dopisując wartość
        # na której skończyło
        while len(bests) < len(max(multiple_bests, key=len)):
            bests.append(bests[-1])

    array_multiple_bests = [np.array(x) for x in multiple_bests]
    means = [np.mean(k) for k in zip(*array_multiple_bests)]

    x = range(1, 1 + len(means))

    plt.scatter(x, means)
    plt.grid()
    plt.xlabel("Liczba iteracji")
    plt.ylabel("Czas najlepszego uzyskanego rozwiązania")
    plt.title(f"Średni czas pracy algorytmu to: {np.round(np.mean(times_measured), 2)}s")
    plt.show()


def plot_results_compare(sheet_name: str, num_of_vehicles: int, num_of_runs: int = 20, num_of_iterations=100,
                         switch_in_all_routes=False):
    graph = excel_to_graph(path=path_date,
                           sheet_name=sheet_name)

    vehicles = []
    for i in range(1, num_of_vehicles + 1):
        vehicles.append(Vehicle(Id=i))

    multiple_bests_bee = []
    times_measured_bee = []

    while len(multiple_bests_bee) < num_of_runs:
        from algorithms import bee_algorithm
        start_time = time.time()
        sol, bests = bee_algorithm.bee_algorythm(graph=graph, vehicles=vehicles, num_of_iterations=num_of_iterations,
                                                 size_of_iteration=20, num_of_elite=3, num_of_bests=5,
                                                 size_of_neighbourhood_elite=5,
                                                 size_of_neighbourhood_best=3, max_LT=2,
                                                 switch_in_all_routes=switch_in_all_routes)
        end_time = time.time()

        times_measured_bee.append(end_time - start_time)
        multiple_bests_bee.append(bests)
        print(f"{len(multiple_bests_bee)}: {sol.time}")
        graph.reset_visited()

    for bests in multiple_bests_bee:  # w każdym uruchomieniu algorytm może skończyć się w różnej liczbie iteracji więc
        # w celu poprawnego wyroswania średniej trzeba dorównać ilość iteracji do tej największej dopisując wartość
        # na której skończyło
        while len(bests) < len(max(multiple_bests_bee, key=len)):
            bests.append(bests[-1])

    array_multiple_bests_bee = [np.array(x) for x in multiple_bests_bee]

    means_bee = [np.mean(k) for k in zip(*array_multiple_bests_bee)]

    x_bee = range(1, 1 + len(means_bee))

    plt.scatter(x_bee, means_bee, label='Algotym pszczeli')
    plt.legend()
    plt.grid()
    plt.xlabel("Liczba iteracji")
    plt.ylabel("Średni czas najlepszego uzyskanego rozwiązania")
    # plt.title()
    plt.show()

    print(f"Średni czas pracy algorytmu pszczelego to: {np.round(np.mean(times_measured_bee), 2)}s")
