import math
import numpy as np
from app.classes.solution import Solution


def parent_selection_roulette(population: list[Solution], population_size: int) -> list[(Solution, Solution)]:
    """ Ruletka: Funkcja wybierająca pary rodziców na podstawie prawdopodobieństwa chromosomów.

     Args:
        population (list[Solution]): Lista rozwiązań
        population_size (int): Rozmiar populacji.

     Returns:
        list[(Solution, Solution)]: Lista par rodziców.
    """

    # Obliczenie prawdopodobieństw chromosomów
    chromosome_probab_all = calculate_chromosome_probabilities(population)
    # Utworzenie słownika indeksów populacji
    population_normalize_all = {idx: solution for idx, solution in enumerate(population)}

    # Lista przechowująca pary rodziców
    parents = []
    # Słownik indeksów użytych rodziców
    parents_index = {idx:[] for idx in range(len(population))}
    for _ in range(population_size):
        population_normalize = population_normalize_all.copy()
        first_parent_index = np.random.choice(list(population_normalize.keys()), p=chromosome_probab_all)

        # Usunięcie indeksu pierwszego rodzica z populacji
        population_normalize.pop(first_parent_index)
        # Sprawdzenie, czy indeks został już użyty
        if parents_index.get(first_parent_index):
            # Usunięcie indeksów użytych z populacji
            for val in parents_index[first_parent_index]:
                population_normalize.pop(val)

        # Obliczenie prawdopodobieństw dla pozostałych chromosomów
        chromosome_probab_second = calculate_chromosome_probabilities(population_normalize.values())
        # Wybór drugiego rodzica na podstawie nowych prawdopodobieństw
        second_parent_index = np.random.choice(list(population_normalize.keys()), p=chromosome_probab_second)

        # Dodanie indeksu drugiego rodzica do listy użytych indeksów
        parents_index.get(first_parent_index).append(second_parent_index)
        # Dodanie pary rodziców do listy wynikowej
        parents.append([population_normalize_all[first_parent_index], population_normalize_all[second_parent_index]])
    return parents


def parent_selection_tournament(population: list[Solution], population_size: int) -> list[(Solution, Solution)]:
    """ Selekcja turniejowa: Funkcja wybierająca pary rodziców poprzez turniej.
         Args:
            population (list[Solution]): Lista rozwiązań
            population_size (int): Rozmiar populacji.

        Returns:
            list[(Solution, Solution)]: Lista par rodziców.
    """
    # Utworzenie słownika indeksów populacji
    population_normalize_all = {idx: solution for idx, solution in enumerate(population)}

    # Słownik indeksów użytych rodziców
    parents_index = {idx: [] for idx in range(len(population))}
    parents = []
    for _ in range(population_size):
        population_normalize = population_normalize_all.copy()
        # Losowy wybór trzech osobników z populacji
        tournament_pool = np.random.choice(list(population_normalize.keys()), 3)
        # Wybór lepszego osobnika z turnieju jako pierwszego rodzica
        first_parent_index = min(tournament_pool, key=lambda x: population_normalize[x].time)
        # Usunięcie indeksu pierwszego rodzica z populacji
        population_normalize.pop(first_parent_index)

        # Sprawdzenie, czy indeks został już użyty
        if parents_index.get(first_parent_index):
            # Usunięcie indeksów użytych z populacji
            for val in parents_index[first_parent_index]:
                population_normalize.pop(val)

        # Losowy wybór trzech osobników z populacji
        tournament_pool = np.random.choice(list(population_normalize.keys()), 3)
        # Wybór drugiego rodzica
        second_parent_index = min(tournament_pool, key=lambda x: population_normalize[x].time)

        # Dodanie indeksu drugiego rodzica do listy użytych indeksów
        parents_index.get(first_parent_index).append(second_parent_index)
        # Dodanie pary rodziców do listy wynikowej
        parents.append([population_normalize_all[first_parent_index], population_normalize_all[second_parent_index]])
    return parents


def children_selection_roulette(parents: list[Solution], childrens: list[Solution], population_size: int, max_parental_involvement: int) -> list[Solution]:
    """ "Selekcja metodą ruletki.

    Args:
        parents (list[Solution]): Lista rodziców.
        childrens (list[Solution]): Lista dzieci.
        population_size (int): Rozmiar populacji.
        max_parental_involvement (int): Maksymalne zaangażowanie rodzicielskie jako procent rozmiaru populacji.

    Returns:
        list[Solution]: Nowe pokolenie.
    """
    #Określenie liczby osobników z pokolenia rodzicielskiego
    parents_number = math.ceil(population_size * max_parental_involvement/100)
    population = parents + childrens

    # Utworzenie słownika indeksów populacji
    population_normalize = {idx:((solution,'p') if idx < len(parents) else (solution, 'c')) for idx, solution in enumerate(population)}
    new_generation = []
    i = 0
    j = 0
    values = []
    # Wybór osobników z pokolenia rodzicielskiego
    while len(new_generation) < population_size:
        # Obliczenie prawdopodobieństw chromosomów

        chromosome_probab = calculate_chromosome_probabilities([tuple[0] for tuple in list(population_normalize.values())])
        index = np.random.choice(list(population_normalize.keys()), p=chromosome_probab)
        if population_normalize[index][0].time not in values or j > 10:
            if population_normalize[index][1] == "p":
                if(i < parents_number):
                    i += 1
                    j = 0
                    values += [population_normalize[index][0].time]
                    # Usunięcie indeksu z populacji i dodanie do rozwiązania osobnika z warstwy rodzicielskiej
                    new_generation.append(population_normalize.pop(index)[0])
            else:
                values += [population_normalize[index][0].time]
                j = 0
                # Usunięcie indeksu z populacji i dodanie do rozwiązania osobnika z warstwy dzieci
                new_generation.append(population_normalize.pop(index)[0])
        else:
            j += 1
    return new_generation


def children_selection_ranking(parents: list[Solution], childrens: list[Solution], population_size: int, max_parental_involvement: int) -> list[Solution]:
    """ Selekcja metodą rankingową.

    Args:
        parents (list[Solution]): Lista rodziców.
        childrens (list[Solution]): Lista dzieci.
        population_size (int): Rozmiar populacji.
        max_parental_involvement (int): Maksymalne zaangażowanie rodzicielskie jako procent rozmiaru populacji.

    Returns:
        list[Solution]: Nowe pokolenie.
    """
    # Określenie liczby osobników z pokolenia rodzicielskiego
    parents_number = math.ceil(population_size * max_parental_involvement / 100)

    parents = [('p', solution) for solution in parents]
    childrens = [('c', solution) for solution in childrens]
    population = parents + childrens
    #sortowanie
    population.sort(key=lambda tuple: tuple[1].time)

    # Tworzenie nowego pokolenia poprzez połączenie najlepszych rodziców i dzieci
    i = 0
    new_generation = list()
    for solution in population:
        if solution[0] == 'p' and i <= parents_number:
            i += 1
            new_generation.append(solution[1])
        elif solution[0] == 'c':
            new_generation.append(solution[1])
        if len(new_generation) == population_size:
            break

    return new_generation

def calculate_chromosome_probabilities(population):
    """Oblicza prawdopodobieństwa chromosomów na podstawie czasu wykonania.

       Args:
           population (list[Solution]): Lista rozwiązań, gdzie każde rozwiązanie ma atrybut `time`.

       Returns:
           list[float]: Lista prawdopodobieństw chromosomów.
       """
    # Znajdź minimalny czas wykonania i odejmij od niego stałą (żeby najlepsze osobniki miały większą szanse na rozmnożenie)
    #TODO
    min_val = min(solution.time for solution in population)-300
    # Oblicz sumę odwrotności czasu wykonania (po odjęciu minimalnego czasu)
    sum_time_all = sum(1 / (solution.time-min_val) for solution in population)
    # Oblicz prawdopodobieństwo dla każdego chromosomu
    chromosome_probab_all = [1 / ((solution.time-min_val) * sum_time_all) for solution in population]
    return chromosome_probab_all