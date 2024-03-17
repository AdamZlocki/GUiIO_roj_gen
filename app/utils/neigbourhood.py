# from random import randint, choice
# from typing import List
#
# from app.classes.edge import Edge
# from app.classes.graph import GraphMatrix
# from app.classes.solution import Solution
# from app.utils.utils_functions import calc_vehicle_time, calc_solution_time

"""W zasadzie to już niepotrzebne ale zostawiam jakby ktoś chciał się czymś zainspirować"""

# def neighbourhood(graph: GraphMatrix, solution: Solution, size: int = 5, switch_in_all_routes=False):
#     """Funkcja do znajdowania losowego sąsiedztwa rozwiązania przy założeniu że każdy z sąsiadów jest rozwiązaniem
#     dopuszczalanym - wymaga modyfikacji na podstawie przyjętych algorytmów"""
#
#     neighbours: List[Solution] = []
#     counter_of_attempts = 0
#     if not switch_in_all_routes:  # zamiana kolejności wierzchołków na trasie jednego pojazdu
#         while len(neighbours) < size:  # pętla powtarzana do utworzenia oczekiwanej liczby sąsiadów
#             neighbours = switch_single_vehicle_route(neighbours, solution, graph, counter_of_attempts)
#
#     else:  # zmiana kolejności na trasie każdego pojazdu
#         while len(neighbours) < size:  # pętla powtarzana do utworzenia oczekiwanej liczby sąsiadów
#             neighbours = switch_all_vehicles_route(neighbours, solution, graph, counter_of_attempts)
#     return neighbours
#
#
# def switch_single_vehicle_route(neighbours, solution, graph, counter_of_attempts):
#     # zamiana kolejności wierzchołków na trasie jednego pojazdu
#
#     if counter_of_attempts > 20 and len(neighbours) >= 1:
#         # jeśli 30 razy z rzędu nie udało się stworzyć sąsiada kończymy pętlę z tyloma
#         # ile się udało -> zapobiega pętli nieskończonej gdy jakieś rozwiązanie ma za mało
#         # dopuszczlanych sąsiadów
#         print(f"utworzono tylko {len(neighbours)} sąsiadów")
#         return neighbours
#
#     vehicle = choice(list(solution.routes.keys()))
#     route = solution.routes[vehicle]
#     new_waiting_times = solution.waiting_times.copy()
#     n = len(route)
#     if n <= 3:  # jeśli trasa ma długość 3 to znaczy że między początkiem a końcem jest tylko jeden punkt więc
#         # zmiana kolejności niemożliwa
#         return neighbours
#     new_route = swap_vertices(route)
#
#     new_edges: List[Edge] = []  # utworzenie nowej listy krawędzi
#     for i in range(1, len(new_route)):
#         vertex_idx1 = new_route[i - 1]
#         vertex_idx2 = new_route[i]
#         new_edges.append(graph.matrix[vertex_idx1][vertex_idx2])
#
#     vehicle_route_is_fine = check_vehicle_route(new_route, graph, vehicle, new_edges, new_waiting_times)
#     if vehicle_route_is_fine:
#         new_time = calc_vehicle_time(graph=graph, routes=new_route, edges=new_edges,
#                                      waiting_times=new_waiting_times[vehicle])
#         routes = solution.routes.copy()
#         routes[vehicle] = new_route
#         neighbour = Solution(routes=routes, time=new_time, waiting_times=new_waiting_times)
#         if neighbour not in neighbours:  # wstawienie nowego sąsiada jeśli nie ma go w sąsiedztwie
#             neighbours.append(neighbour)
#             counter_of_attempts = 0
#         else:
#             counter_of_attempts += 1
#     else:
#         counter_of_attempts += 1
#
#     return neighbours
#
#
# def swap_vertices(route):
#     a, b = 0, 0
#     while a == b:  # wylosowanie punktów do podmiany
#         a, b = randint(1, len(route) - 2), randint(1, len(route) - 2)
#     new_route = route.copy()
#     new_route[a], new_route[b] = new_route[b], new_route[a]
#     return new_route
#
#
# def check_vehicle_route(new_route, graph, vehicle, new_edges, new_waiting_times):
#     # sprawdzenie czy nadal pojazd przyjeżdża o odpowiedniej porze
#     vehicle.reset_free_at()
#     for i in range(1, len(new_route)):
#         edge_time = new_edges[i - 1].time
#         next_vertex = graph.get_vertex(new_route[i])
#         time_at_place = vehicle.free_at + edge_time
#         if time_at_place >= next_vertex.time_window[1]:  # pojazd przyjeżdża zbyt późno
#             return False
#         else:
#             if time_at_place < next_vertex.time_window[0]:  # pojazd przyeżdża zbyt wcześnie
#                 new_waiting_times[vehicle][new_route[i]] = next_vertex.time_window[0] - time_at_place
#             else:  # pojazd przyjeżdża w oknie czasowym
#                 new_waiting_times[vehicle][new_route[i]] = 0
#             vehicle.free_at += edge_time + next_vertex.service_time + new_waiting_times[vehicle][new_route[i]]
#     return True
#
#
# def switch_all_vehicles_route(neighbours, solution, graph, counter_of_attempts):
#     # zmiana kolejności na trasie każdego pojazdu
#     if counter_of_attempts > 20 and len(neighbours) >= 1:
#         print(f"utworzono tylko {len(neighbours)} sąsiadów")
#         return neighbours
#
#     new_times = {}
#     new_routes = solution.routes.copy()
#     new_waiting_times = solution.waiting_times.copy()
#     for vehicle in solution.routes.keys():  # dla każdego pojazdu zmieniana jest jego trasa
#         counter_of_attempts_vehicle = 0
#         while new_routes[vehicle] == solution.routes[vehicle] and counter_of_attempts_vehicle < 20:
#             # próby zmiany trasy do skutku
#             new_route = solution.routes[vehicle].copy()  # podmiana wybranych wierzchołków
#             n = len(new_route)
#             if n <= 3:  # jeśli trasa ma długość 3 to znaczy że między początkiem a końcem jest tylko jeden
#                 # punkt więc zmiana kolejności niemożliwa
#                 break
#             new_route = swap_vertices(new_route)
#             new_edges: List[Edge] = []  # utworzenie nowej listy krawędzi
#             vehicle_route_is_fine = check_vehicle_route(new_route, graph, vehicle, new_edges, new_waiting_times)
#             if vehicle_route_is_fine:
#                 new_times[vehicle] = calc_vehicle_time(graph=graph, routes=new_route, edges=new_edges,
#                                                        waiting_times=new_waiting_times[vehicle])
#                 new_routes[vehicle] = new_route
#             else:
#                 counter_of_attempts_vehicle += 1
#
#     neighbour = Solution(routes=new_routes, time=calc_solution_time(new_times), waiting_times=new_waiting_times)
#     if neighbour not in neighbours:
#         neighbours.append(neighbour)
#     else:
#         counter_of_attempts += 1
#
#     return neighbours
