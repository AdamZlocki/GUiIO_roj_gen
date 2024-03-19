from typing import Dict, List
from app.classes.solution import Solution
from app.classes.vehicle import Vehicle


def cso_step(cockroach_to_move: Dict[Vehicle, List[int]], destination: Dict[Vehicle, List[int]], vehicle_order: List[Vehicle]):
    """Modyfikuje pierwszego karalucha (cockroach_to_move) robiąc krok w stronę drugiego (destination)"""
    for vehicle in vehicle_order:

        ctm_vehicle, dest_vehicle = cockroach_to_move[vehicle], destination[vehicle]
        for i, dest_vertex in enumerate(dest_vehicle):

            if i > len(ctm_vehicle) - 1:
                ctm_vehicle.append(dest_vertex)
                _cso_step_remove_duplicate(cockroach_to_move, i, vehicle, dest_vertex, vehicle_order)
                return
            elif dest_vertex != ctm_vehicle[i]:
                val_to_replace = ctm_vehicle[i]
                ctm_vehicle[i] = dest_vertex
                _cso_step_remove_duplicate(cockroach_to_move, i, vehicle, dest_vertex, vehicle_order, val_to_replace)
                return

    print("Rozwiązania są identyczne - nie wykonano kroku")


# Funkcja potrzebna tylko do cso_step_towards
def _cso_step_remove_duplicate(sol_routes: Dict[Vehicle, List[int]], keep_vertex_ind, keep_vertex_veh, keep_vertex_val, vehicle_order, new_val=None):
    for vehicle in vehicle_order:

        for i, vertex in enumerate(sol_routes[vehicle]):

            # Jeżeli wartość jest ta sama ale indeks albo pojazd się nie zgadza to trzeba go wywalić (a częściej zamienić na ten co został wcześniej zmieniony)
            if vertex == keep_vertex_val and (i != keep_vertex_ind or vehicle != keep_vertex_veh):
                if new_val is None:
                    del sol_routes[vehicle][i]
                else:
                    sol_routes[vehicle][i] = new_val
                return

