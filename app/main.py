from utils.utils_functions import plot_results_compare, plot_results
from algorithms import genetic_algorithm


def main():
    # plot_results_compare(sheet_name='Dane 4', num_of_vehicles=4, num_of_runs=1, num_of_iterations=100)


    # plot_results(sheet_name='Dane 4', num_of_vehicles=3, algorithm='bee', num_of_runs=1)
    genetic_algorithm.genetic_algorithm()



if __name__ == '__main__':
    main()
