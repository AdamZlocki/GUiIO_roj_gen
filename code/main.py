from random import choice, randint
from typing import Dict, List
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt


class Vertex:
    """wierzchołek - reprezentowany przez id, informuje o swoim położeniu, czasie trwania serwisu i oknach czasowych"""
    def __init__(self, Id, x: (int, float), y: (int, float), time_window: tuple, service_time: (int, float),
                 is_base=False):
        if not is_base:
            self.Id = Id
            self.x = x
            self.y = y
            self.visited = 0
            self.time_window = time_window
            self.service_time = service_time
        else:
            self.Id = Id
            self.x = x
            self.y = y
            self.visited = 1
            self.time_window = time_window
            self.service_time = service_time

    def __eq__(self, other):
        if self.Id == other.Id:
            return True
        else:
            return False

    def __repr__(self):
        return f"{self.Id}"

    def __hash__(self):
        return hash(self.Id)


class Edge:
    """połączenie między wierzchołkami; reprezentuje czas przejazdu"""
    def __init__(self, start, end, time: float = 0):
        self.start = start
        self.end = end
        self.time = time

    def __eq__(self, other):
        if self.start == other.start and self.end == other.end:
            return True
        else:
            return False

    def __repr__(self):
        return f"({self.start} -- {self.time} --> {self.end})"


class Vehicle:
    """pojazd; reprezentowany przez id i informuje o której może jechać do kolejnego wierzchołka"""
    def __init__(self, Id, free_at=0):
        self.Id = Id
        self.free_at = free_at

    def __eq__(self, other):
        if self.Id == other.Id:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.Id)

    def __repr__(self):
        return f"{self.Id}"

    def reset_free_at(self):
        self.free_at = 0


class GraphMatrix:
    """graf - jak na labach Pawlika składa się z listy wierzhcołków, macierzy krawędzi i słownika"""
    def __init__(self):
        self.list: List[Vertex] = []
        self.dict = {}
        self.matrix: List[List[Edge or int]] = [[]]

    def insertVertex(self, vertex: Vertex):
        self.list.append(vertex)
        self.dict[vertex] = self.order() - 1
        if self.order() != 1:
            for i in range(len(self.matrix)):
                self.matrix[i].append(0)
            self.matrix.append([0] * len(self.matrix[0]))
        else:
            self.matrix[0].append(0)

    def insertEdge(self, vertex1_idx: int, vertex2_idx: int, edge: Edge):
        if vertex1_idx is not None and vertex2_idx is not None and edge is not None:
            self.matrix[vertex1_idx][vertex2_idx] = edge

    # def deleteVertex(self, vertex):
    #     vertex_idx = self.getVertexIdx(vertex)
    #     for i in range(self.order()):
    #         if i != vertex_idx:
    #             self.matrix[i].pop(vertex_idx)
    #     self.matrix.pop(vertex_idx)
    #     self.list.pop(vertex_idx)
    #     self.dict.pop(vertex)
    #     for i in range(vertex_idx, self.order()):
    #         actual = self.list[i]
    #         self.dict[actual] -= 1
    #
    # def deleteEdge(self, vertex1, vertex2):
    #     vertex1_idx = self.getVertexIdx(vertex1)
    #     vertex2_idx = self.getVertexIdx(vertex2)
    #     for i in range(len(self.matrix[vertex1_idx])):
    #         if self.matrix[vertex1_idx][vertex2_idx] != 0:
    #             self.matrix[vertex1_idx][vertex2_idx] = 0

    def getVertexIdx(self, vertex):
        return self.dict[vertex]

    def getVertex(self, vertex_idx) -> Vertex:
        return self.list[vertex_idx]

    def neighbours(self, vertex_idx) -> List[int]:  # zwraca indeksy w macierzy sąsiadów wybranego wierzchołka
        result = []
        for i in range(len(self.matrix[vertex_idx])):
            if self.matrix[vertex_idx][i]:
                result.append(i)
        return result

    def order(self):
        return len(self.list)

    def size(self):
        result = 0
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] != 0:
                    result += 1
        return result

    def edges(self):
        result = []
        for i in range(self.order()):
            for j in range(self.order()):
                if self.matrix[i][j]:
                    result.append(self.matrix[i][j])
        return result

    def reset_visited(self):
        for vertex in self.list[1:]:
            vertex.visited = 0


class Solution:
    """reprezentacja danego rozwiązania - routes to ścieżki przeybywane przez każdy z pojazdów, waiting_times to czas
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


def calc_solution_time(times: dict) -> int:
    """wybiera czas rowiązania na podstawie czasów każdego z pojazdów"""
    return max(times.values())


def calc_vehicle_time(graph: GraphMatrix, routes, edges, waiting_times) -> float:
    """czas = suma czasów serwisu + łączny czas oczekiwania + łączny czas krawędzi (wszystko dla danego pojazdu)"""
    service_times = []
    for vertex_idx in routes:
        vertex = graph.getVertex(vertex_idx=vertex_idx)
        service_times.append(vertex.service_time)
    time = sum(service_times) + sum(list(waiting_times.values()))
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


def find_solution(graph: GraphMatrix, vehicles: List[Vehicle]):
    """funkcja do znajdowania losowego rozwiązania w przestrzeni rozwiązań przy założeniu że jest ono dopuszczalane"""
    routes: Dict[Vehicle, list] = {}
    edges: Dict[Vehicle, List[Edge]] = {}
    currents: Dict[Vehicle, int] = {}
    times: Dict[Vehicle, float] = {}
    waiting_times: Dict[Vehicle, Dict[int, float]] = {}
    for vehicle in vehicles:  # inicjalizacja list dla każdego pojazdu w słownikach
        routes[vehicle] = [0]
        edges[vehicle] = []
        currents[vehicle] = 0
        times[vehicle] = 0
        waiting_times[vehicle] = {}

    while not all_visited(graph):  # pętla wykonywana dopóki nie wszystkie wierzchołki są odwiedzone
        old_currents = currents.copy()
        for vehicle in vehicles:
            if not (currents[vehicle] == 0 and len(
                    routes[vehicle]) > 1):  # jeśli trasa jest dłuższa niż 1 wierzchołek i na
                # końcu jest 0 to znaczy że trasa dla tego pojazdu jest już skończona
                current = currents[vehicle]

                neighbours = graph.neighbours(current)  # wyszukanie sąsiadów i usunięcie wierzchołka Bazy
                if 0 in neighbours:
                    neighbours.remove(0)

                neighbours_to_delete = []  # wyszukanie już odwiedzonych sąsiadów lub sąsiadów z niepasującym oknem
                # czasowym
                for neigh in neighbours:
                    edge_time = graph.matrix[current][neigh].time
                    neigh_Vertex = graph.getVertex(neigh)
                    time_at_place = vehicle.free_at + edge_time
                    if neigh_Vertex.visited == 1 or not (time_at_place < neigh_Vertex.time_window[1]):
                        neighbours_to_delete.append(neigh)

                for neigh in neighbours_to_delete:  # usunięcie niedozwolonych sąsiadów
                    neighbours.remove(neigh)

                if len(neighbours):  # jeśli zostali jeszcze jacyś sąsiedzi wylosowanie nastepnego wierzchołka
                    neighbour = choice(neighbours)
                    neigh_Vertex = graph.getVertex(neighbour)
                    edge_time = graph.matrix[current][neighbour].time
                    time_at_place = vehicle.free_at + edge_time
                    # sprawdzenie czy pojazd nie przyjedzie przed rozpoczęciem okna czasowego
                    if time_at_place < neigh_Vertex.time_window[0]:
                        waiting_times[vehicle][neighbour] = neigh_Vertex.time_window[0] - time_at_place
                    else:
                        waiting_times[vehicle][neighbour] = 0
                    graph.getVertex(neighbour).visited = 1
                    vehicle.free_at += edge_time + neigh_Vertex.service_time + waiting_times[vehicle][neighbour]
                else:  # jeśli nie -> wybranie 0 i powrót do bazy
                    neighbour = 0

                edges[vehicle].append(graph.matrix[current][neighbour])  # aktualizacja tablic dla danego pojazdu
                routes[vehicle].append(neighbour)
                currents[vehicle] = neighbour

        if old_currents == currents:  # jeśli nie dodano żadnego nowego punktu na trasach -> reset słowników, czasów
            # pojazdów i odwiedzenia wierzchołków
            graph.reset_visited()
            for vehicle in vehicles:
                routes[vehicle] = [0]
                edges[vehicle] = []
                currents[vehicle] = 0
                times[vehicle] = 0
                waiting_times[vehicle] = {}
                vehicle.reset_free_at()
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


def neighbourhood(graph: GraphMatrix, solution: Solution, size: int = 5, switch_in_all_routes=False):
    """funkcja do znajdowania losowego sąsiedztwa rozwiązania przy założeniu że każdy z sąsiadów jest rozwiązaniem
    dopuszczalanym - wymaga modyfikacji na podstawie przyjętych algorytmów"""

    neighbours: List[Solution] = []
    counter_of_attempts = 0
    if not switch_in_all_routes:  # zamiana kolejności wierzchołków na trasie jednego pojazdu
        while len(neighbours) < size:  # pętla powtarzana do utworzenia oczekiwanej liczby sąsiadów
            if counter_of_attempts > 20 and len(
                    neighbours) >= 1:  # jeśli 30 razy z rzędu nie udało się stworzyć sąsiada kończymy pętlę z tyloma
                # ile się udało -> zapobiega pętli nieskończonej gdy jakieś rozwiązanie ma za mało
                # dopuszczlanych sąsiadów
                print(f"utworzono tylko {len(neighbours)} sąsiadów")
                break

            vehicle = choice(list(solution.routes.keys()))
            route = solution.routes[vehicle]
            new_waiting_times = solution.waiting_times.copy()
            n = len(route)
            if n <= 3:  # jeśli trasa ma długość 3 to znaczy że między początkiem a końcem jest tylko jeden punkt więc
                # zmiana kolejności niemożliwa
                continue
            a, b = 0, 0
            while a == b:  # wylosowanie punktów do podmiany
                a, b = randint(1, n - 2), randint(1, n - 2)

            new_route = route.copy()  # podmiana wybranych wierzchołków
            new_route[a], new_route[b] = new_route[b], new_route[a]

            new_edges: List[Edge] = []  # utworzenie nowej listy krawędzi
            for i in range(1, len(new_route)):
                vertex_idx1 = new_route[i - 1]
                vertex_idx2 = new_route[i]
                new_edges.append(graph.matrix[vertex_idx1][vertex_idx2])

            vehicle_route_is_fine = True  # sprawdzenie czy nadal pojazd przyjeżdża o odpowiedniej porze
            vehicle.reset_free_at()
            for i in range(1, len(new_route)):
                edge_time = new_edges[i - 1].time
                next_Vertex = graph.getVertex(new_route[i])
                time_at_place = vehicle.free_at + edge_time
                if not (time_at_place < next_Vertex.time_window[1]):  # pojazd przyjeżdża zbyt późno
                    vehicle_route_is_fine = False
                    break
                else:
                    if time_at_place < next_Vertex.time_window[0]:  # pojazd przyeżdża zbyt wcześnie
                        new_waiting_times[vehicle][new_route[i]] = next_Vertex.time_window[0] - time_at_place
                    else:  # pojazd przyjeżdża w oknie czasowym
                        new_waiting_times[vehicle][new_route[i]] = 0
                    vehicle.free_at += edge_time + next_Vertex.service_time + new_waiting_times[vehicle][new_route[i]]

            if vehicle_route_is_fine:
                new_time = calc_vehicle_time(graph=graph, routes=new_route, edges=new_edges,
                                             waiting_times=new_waiting_times[vehicle])
                routes = solution.routes.copy()
                routes[vehicle] = new_route
                neighbour = Solution(routes=routes, time=new_time, waiting_times=new_waiting_times)
                if neighbour not in neighbours:  # wstawienie nowego sąsiada jeśli nie ma go w sąsiedztwie
                    neighbours.append(neighbour)
                    counter_of_attempts = 0
                else:
                    counter_of_attempts += 1
            else:
                counter_of_attempts += 1

    else:  # zmiana kolejności na trasie każdego pojazdu
        while len(neighbours) < size:  # pętla powtarzana do utworzenia oczekiwanej liczby sąsiadów
            if counter_of_attempts > 20 and len(
                    neighbours) >= 1:  # jeśli 20 razy z rzędu nie udało się stworzyć sąsiada kończymy pętlę z tyloma
                # ile się udało -> zapobiega pętli nieskończonej gdy jakieś rozwiązanie ma za mało
                # dopuszczlanych sąsiadów
                print(f"utworzono tylko {len(neighbours)} sąsiadów")
                break

            new_times = {}
            new_routes = solution.routes.copy()
            new_waiting_times = solution.waiting_times.copy()
            for vehicle in solution.routes.keys():  # dla każdego pojazdu zmieniana jest jego trasa
                counter_of_attempts_vehicle = 0
                while new_routes[vehicle] == solution.routes[
                    vehicle] and counter_of_attempts_vehicle < 20:  # próby zmiany trasy do skutku
                    new_route = solution.routes[vehicle].copy()  # podmiana wybranych wierzchołków
                    n = len(new_route)
                    if n <= 3:  # jeśli trasa ma długość 3 to znaczy że między początkiem a końcem jest tylko jeden
                        # punkt więc zmiana kolejności niemożliwa
                        break
                    a, b = 0, 0
                    while a == b:  # wylosowanie punktów do podmiany
                        a, b = randint(1, n - 2), randint(1, n - 2)
                    new_route[a], new_route[b] = new_route[b], new_route[a]

                    new_edges: List[Edge] = []  # utworzenie nowej listy krawędzi
                    for i in range(1, len(new_route)):
                        vertex_idx1 = new_route[i - 1]
                        vertex_idx2 = new_route[i]
                        new_edges.append(graph.matrix[vertex_idx1][vertex_idx2])

                    vehicle_route_is_fine = True  # sprawdzenie czy nadal pojazd przyjeżdża o odpowiedniej porze
                    vehicle.reset_free_at()
                    for i in range(1, len(new_route)):
                        edge_time = new_edges[i - 1].time
                        next_Vertex = graph.getVertex(new_route[i])
                        time_at_place = vehicle.free_at + edge_time
                        if not (time_at_place < next_Vertex.time_window[1]):  # pojazd przyjeżdża zbyt późno
                            vehicle_route_is_fine = False
                            break
                        else:
                            if time_at_place < next_Vertex.time_window[0]:  # pojazd przyeżdża zbyt wcześnie
                                new_waiting_times[vehicle][new_route[i]] = next_Vertex.time_window[0] - time_at_place
                            else:  # pojazd przyjeżdża w oknie czasowym
                                new_waiting_times[vehicle][new_route[i]] = 0
                            vehicle.free_at += edge_time + next_Vertex.service_time + new_waiting_times[vehicle][
                                new_route[i]]

                    if vehicle_route_is_fine:
                        new_times[vehicle] = calc_vehicle_time(graph=graph, routes=new_route, edges=new_edges,
                                                               waiting_times=new_waiting_times[vehicle])
                        new_routes[vehicle] = new_route
                    else:
                        counter_of_attempts_vehicle += 1

            neighbour = Solution(routes=new_routes, time=calc_solution_time(new_times), waiting_times=new_waiting_times)
            if neighbour not in neighbours:  # wstawienie nowego sąsiada jeśli nie ma go w sąsiedztwie
                neighbours.append(neighbour)
            else:
                counter_of_attempts += 1
    return neighbours


def calculate_edge_time(vertex1: Vertex, vertex2: Vertex):
    """zakładamy prędkość 1 kilometr na minutę -> czas [min] = dystans [km]"""
    return round(np.sqrt((vertex2.x - vertex1.x) ** 2 + (vertex2.y - vertex1.y) ** 2), 2)


def excel_to_graph(path: str, sheet_name: str):
    """czas serwisowania i okna czasowe są w minutach; x i y w kilometrach"""
    data = pd.read_excel(path, sheet_name=sheet_name)
    depot = data.iloc[0, :]
    clients = data.iloc[1:, :]
    graph = GraphMatrix()
    graph.insertVertex(
        Vertex(Id=depot['StringID'], x=depot['x'], y=depot['y'], time_window=(depot['ReadyTime'], depot['DueDate']),
               service_time=depot['ServiceTime'], is_base=True))

    for client_idx in range(clients.shape[0]):
        client = clients.iloc[client_idx]
        graph.insertVertex(Vertex(Id=client['StringID'], x=client['x'], y=client['y'],
                                  time_window=(client['ReadyTime'], client['DueDate']),
                                  service_time=client['ServiceTime']))

    for idx, vertex in enumerate(graph.list):
        for idx2, vertex2 in enumerate(graph.list[idx + 1:]):
            real_idx2 = idx2 + idx + 1
            edge_time = calculate_edge_time(vertex1=vertex, vertex2=vertex2)
            graph.insertEdge(vertex1_idx=idx, vertex2_idx=real_idx2,
                             edge=Edge(start=vertex, end=vertex2, time=edge_time))
            graph.insertEdge(vertex1_idx=real_idx2, vertex2_idx=idx,
                             edge=Edge(start=vertex2, end=vertex, time=edge_time))

    return graph


def plot_results(sheet_name: str, num_of_vehicles: int, algorithm: str, num_of_runs: int = 20,
                 switch_in_all_routes=False):
    graph = excel_to_graph(path=r"C:\Users\adamz\Desktop\Praca_inzynierska\dane\Dane_VRP_WT_ST.xlsx",
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
            import bee_algorithm

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
        for vehicle in vehicles:
            vehicle.reset_free_at()

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
    graph = excel_to_graph(path=r"C:\Users\adamz\Desktop\Głębokie uczenie i Inteligencja obliczeniowa\GUiIO_roj_gen\dane\Dane_VRP_WT_ST.xlsx",
                           sheet_name=sheet_name)

    vehicles = []
    for i in range(1, num_of_vehicles + 1):
        vehicles.append(Vehicle(Id=i))

    multiple_bests_bee = []
    times_measured_bee = []

    while len(multiple_bests_bee) < num_of_runs:
        import bee_algorithm
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
        for vehicle in vehicles:
            vehicle.reset_free_at()

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


def main():
    # plot_results_compare(sheet_name='Dane 2', num_of_vehicles=39, num_of_runs=20, num_of_iterations=100)

    plot_results(sheet_name='Dane 4', num_of_vehicles=3, algorithm='bee', num_of_runs=1)


if __name__ == '__main__':
    main()
