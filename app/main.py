from utils.utils_functions import plot_results_compare, plot_results


def main():
    # plot_results_compare(sheet_name='Dane 4', num_of_vehicles=4, num_of_runs=1, num_of_iterations=100)

    plot_results(sheet_name='Dane 4', num_of_vehicles=3, algorithm='ga', num_of_runs=1)

    # genetic_algorithm.create_new_solution()


if __name__ == '__main__':
    main()
