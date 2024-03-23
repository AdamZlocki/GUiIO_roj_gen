from app.classes.vehicle import Vehicle
from app.classes.solution import Solution
from app.utils.cso_functions import cso_step
from app.utils.cso_functions import cso_get_step_distance

if __name__ == '__main__':

    # # Stwórz graf
    # path_date = r"../dane/Dane_VRP_WT_ST.xlsx"
    # sheet_name = 'Dane 4'
    # graph = excel_to_graph(path=path_date, sheet_name=sheet_name)

    # Stwórz pojazdy
    num_of_vehicles = 3
    vehicles = []
    for i in range(1, num_of_vehicles + 1):
        vehicles.append(Vehicle(Id=i))

    # przykładowe rozwiązania
    # sol1 = {vehicles[0]: [1, 4], vehicles[1]: [5, 3, 2]}
    # sol2 = {vehicles[0]: [5, 1, 2], vehicles[1]: [4, 3]}

    sol1 = Solution({vehicles[0]: [2, 5], vehicles[1]: [9, 3, 8, 7], vehicles[2]: [4, 1, 6]})
    sol2 = Solution({vehicles[0]: [9, 8, 5, 1, 2], vehicles[1]: [4, 3], vehicles[2]: [7, 6]})

    print(f"Dystans w krokach = {cso_get_step_distance(sol1, sol2, vehicles)}")

    print("\nRozwiązanie do którego dążymy")
    for route in sol2.routes.values():
        print(route)

    print("\nRozwiązanie które przemieszczamy")
    for route in sol1.routes.values():
        print(route)

    no_steps = 0
    while sol1 != sol2:
        sol1 = cso_step(sol1, sol2, vehicles) # Wykonanie kroku
        no_steps += 1
        print(f"\nKrok {no_steps}")
        for route in sol1.routes.values():
            print(route)
