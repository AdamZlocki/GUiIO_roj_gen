from app.algorithms.cso_algorithm import cso_algorithm
from app.classes.vehicle import Vehicle
from app.utils.utils_functions import plot_results_compare, excel_to_graph


def main():
    plot_results_compare(sheet_name='Dane 4', num_of_vehicles=4, num_of_runs=1, num_of_iterations=100)

    # plot_results(sheet_name='Dane 4', num_of_vehicles=3, algorithm='bee', num_of_runs=1)


def execute_cso():
    path_date = r"../dane/Dane_VRP_WT_ST.xlsx"
    sheet_name = 'Dane 4'
    num_of_vehicles = 3
    vehicles = []
    for i in range(1, num_of_vehicles + 1):
        vehicles.append(Vehicle(Id=i))
    graph = excel_to_graph(path=path_date, sheet_name=sheet_name)
    sol, best = cso_algorithm(graph=graph,
                              vehicles=vehicles,
                              visual=1,
                              num_of_iterations=3,
                              size_of_iteration=1,
                              max_step=2,
                              vehicles_number=num_of_vehicles,
                              inner_w=1)
    return sol, best


if __name__ == '__main__':
    # main()
    sol, best = execute_cso()
    print(f'{sol=}')
    print(f'{best=}')
