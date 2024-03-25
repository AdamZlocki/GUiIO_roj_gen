from typing import Dict, List
from app.classes.solution import Solution
from app.classes.vehicle import Vehicle
from copy import deepcopy
import random


def dispersal(probability, actual_cockroach: Solution, vehicle_order: List[Vehicle]):
    """Wywołanie rozproszenia z zadanym prawdopodobieństwem - Z każdego samochodu bierzemy losowe miasto i zamieniamy je z innym losowym samochodem"""
    actual_cockroach_copy = deepcopy(actual_cockroach.routes)
    generated_number = random.uniform(0, 0.99)
    if generated_number < probability:
        moved_elem = set()
        for vehicle in vehicle_order:
            cockroach_data = actual_cockroach_copy[vehicle]

            random_index = random.randint(0, len(cockroach_data) - 1)
            random_element = cockroach_data[random_index]

            # Element który już raz został przeniesiony nie może zostać przeniesiony ponownie.
            while random_element in moved_elem:
                random_index = random.randint(0, len(cockroach_data) - 1)
                random_element = cockroach_data[random_index]

            moved_elem.add(random_element)

            other_vehicle = random.choice([v for v in vehicle_order if v != vehicle])

            other_index = random.randint(0, len(actual_cockroach_copy[other_vehicle]) - 1)

            actual_cockroach_copy[vehicle].remove(random_element)
            actual_cockroach_copy[other_vehicle].insert(other_index, random_element)

        if are_routes_acceptable(actual_cockroach_copy):
            return Solution(actual_cockroach_copy)
    else:
        return Solution(actual_cockroach_copy)


class IncorrectSolutionException(Exception):
    pass


def are_routes_acceptable(solution: Dict[Vehicle, List[int]]) -> bool:
    """Zwraca True jeżeli wierzchołki się nie powtarzają i ich nie brakuje (oraz nie ma zera)"""
    vertex_list = []
    for route in solution.values():
        vertex_list += route
    if len(vertex_list) != len(set(vertex_list)):
        return False
    if max(vertex_list) != len(vertex_list):
        return False
    if 0 in vertex_list:
        return False
    return True


def is_routes_pair_acceptable(solution1: Dict[Vehicle, List[int]], solution2: Dict[Vehicle, List[int]]):
    """Zwraca True jeżeli oba rozwiązania są poprawne, oraz zawierają taką samą liczbę wierzchołków"""
    if not are_routes_acceptable(solution1) or not are_routes_acceptable(solution2):
        return False
    if len([ver for route in solution1.values() for ver in route]) != len([ver for route in solution2.values() for ver in route]):
        return False
    return True


def cso_step(cockroach_to_move: Solution, destination: Solution, vehicle_order: List[Vehicle]) -> Solution:
    """Zwraca rozwiązanie powstałe w wyniku kroku pierwszego rozwiązania (cockroach_to_move) w stronę drugiego (destination)"""
    cockroach_to_move_routes_copy = deepcopy(cockroach_to_move.routes)
    _cso_route_step(cockroach_to_move_routes_copy, destination.routes, vehicle_order)
    return Solution(cockroach_to_move_routes_copy)


def _cso_route_step(cockroach_to_move_routes: Dict[Vehicle, List[int]], destination_routes: Dict[Vehicle, List[int]], vehicle_order: List[Vehicle]):
    """Modyfikuje pierwszego karalucha (cockroach_to_move - ścieżki) robiąc krok w stronę drugiego (destination)"""
    if not is_routes_pair_acceptable(cockroach_to_move_routes, destination_routes):
        raise IncorrectSolutionException

    for vehicle in vehicle_order:
        ctm_vehicle, dest_vehicle = cockroach_to_move_routes[vehicle], destination_routes[vehicle]
        for i, dest_vertex in enumerate(dest_vehicle):
            if i > len(ctm_vehicle) - 1:
                ctm_vehicle.append(dest_vertex)
                _cso_step_remove_duplicate(cockroach_to_move_routes, i, vehicle, dest_vertex, vehicle_order)
                return
            elif dest_vertex != ctm_vehicle[i]:
                val_to_replace = ctm_vehicle[i]
                ctm_vehicle[i] = dest_vertex
                _cso_step_remove_duplicate(cockroach_to_move_routes, i, vehicle, dest_vertex, vehicle_order, val_to_replace)
                return

    # print("Rozwiązania są identyczne - nie wykonano kroku")


# Funkcja potrzebna tylko do cso_step_towards
def _cso_step_remove_duplicate(sol_routes: Dict[Vehicle, List[int]], keep_vertex_ind, keep_vertex_veh, keep_vertex_val, vehicle_order, new_val=None):
    for vehicle in vehicle_order:
        for i, vertex in enumerate(sol_routes[vehicle]):
            # Jeżeli wartość jest ta sama ale indeks albo pojazd się nie zgadza to trzeba wywalić (a częściej zamienić na ten co został wcześniej zmieniony)
            if vertex == keep_vertex_val and (i != keep_vertex_ind or vehicle != keep_vertex_veh):
                if new_val is None:
                    del sol_routes[vehicle][i]
                else:
                    sol_routes[vehicle][i] = new_val
                return


def cso_get_step_distance(cockroach_to_move: Solution, destination: Solution, vehicle_order: List[Vehicle], max_distance=100) -> int:
    """Zwraca dystans w liczbie kroków między dwoma karaluchami.
    Kolejność działania ma znaczenie - dystans jest liczony z perspektywy pierwszego karalucha (pierwszego argumentu funkcji).
    Dystans może być inny jeżeli zamienimy karaluchy miejscami"""

    cockroach_to_move_routes = cockroach_to_move.routes
    destination_routes = destination.routes

    if not is_routes_pair_acceptable(cockroach_to_move_routes, destination_routes):
        raise IncorrectSolutionException

    cockroach_to_move_routes_copy = deepcopy(cockroach_to_move_routes)
    no_steps = 0
    while cockroach_to_move_routes_copy != destination_routes:
        if no_steps > max_distance:
            print("Przekroczono maksymalną liczbę kroków")
            return -1
        _cso_route_step(cockroach_to_move_routes_copy, destination_routes, vehicle_order)
        no_steps += 1
    return no_steps
