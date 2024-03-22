from app.classes.vehicle import Vehicle
from app.utils.cso_functions import dispersal

if __name__ == "__main__":

    # Stwórz pojazdy
    num_of_vehicles = 4
    vehicles = []
    for i in range(1, num_of_vehicles + 1):
        vehicles.append(Vehicle(Id=i))

    # Przykładowe rozwiązania
    # sol1 = {vehicles[0]: [1, 4], vehicles[1]: [5, 3, 2], vehicles[2]: [7, 6, 8]}
    # sol2 = {vehicles[0]: [5, 1, 2], vehicles[1]: [4, 3]}
    sol3 = {vehicles[0]: [1, 4], vehicles[1]: [5, 3, 2], vehicles[2]: [7, 6, 8], vehicles[3]: [9, 10, 11, 12]}

    # Wywołanie funckji disperal
    solution = dispersal(probability=1,actual_cockroach=sol3, vehicle_order=vehicles)
    print(solution)

