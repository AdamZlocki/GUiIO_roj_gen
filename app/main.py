from app.utils.utils_functions import plot_results_compare, plot_results


def main():
    plot_results_compare(sheet_name='Dane 2', num_of_vehicles=39, num_of_runs=2, num_of_iterations=100)

    # plot_results(sheet_name='Dane 4', num_of_vehicles=3, algorithm='bee', num_of_runs=1)


if __name__ == '__main__':
    main()
