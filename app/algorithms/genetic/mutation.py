from app.classes.solution import Solution
import random


def mutation_1(population: list[Solution], probability: float) -> list[Solution]:
    """
    Mutacja: Zadaniem tego operatora mutacji jest dokonanie mutacji, o ile
    liczba losowana w ramach funkcji reprezentującej ten operator będzie mniejsza
    lub równa wartości prawdopodobieństwa będącego parametrem wejściowym. Obie
    wartości są znormalizowane do przedziału [0,1]. W tym wariancie mutacja polega
    na wylosowaniu wierzchołka z dowolnego pojazdu i przeniesieniu go na losową pozycję
    w dowolnym samochodzie (miejsce może nie ulec zmianie). Jedynym ograniczeniem jest sytuacja,
    gdy byłby to jedyny wierzchołek w danym pojeździe. Wtedy operator mutacji zostaje
    zastosowany ponownie aż do znalezienia właściwego wierzchołka.

    Args:
        population: Lista osobników powstałych w wyniku zajścia operatora krzyżowania
        probability: Prawdopodobieństwo zajścia mutacji znormalizowana do przedziału [0,1]

    Returns:
        Lista osobników po zajściu mutacji. Mutacja mogła nie wystąpić i w takim wypadku
        dany osobnik nie ulega modyfikacji.

    """
    mutated_population = []
    for solution in population:
        # Sprawdzenie, czy mutacja wystąpi
        if random.random() <= probability:
            # Usunięcie 0 z początku i końca listy
            routes = {vehicle: route[1:-1] for vehicle, route in solution.routes.items()}

            # Wybierz które ścieżki biorą udział w mutacji (długość > 1)
            eligible_routes = {vehicle: route for vehicle, route in routes.items() if len(route) > 1}

            if eligible_routes:
                # Wybór losowego wierzchołka do przeniesienia
                from_vehicle, from_route = random.choice(list(eligible_routes.items()))
                vertex_index = random.randint(0, len(from_route) - 1)
                vertex = from_route.pop(vertex_index)

                # Wybór docelowej ścieżki
                to_vehicle, to_route = random.choice(list(routes.items()))
                insert_index = random.randint(0, len(to_route))

                # Umieszczenie wierzchołka w nowym miejscu
                to_route.insert(insert_index, vertex)

                # Dodanie 0 na powrót w celu utworzenia pełnych rozwiązań
                mutated_solution = Solution(
                    routes={vehicle: [0] + route + [0] for vehicle, route in routes.items()})
            else:
                # Jeśli nie ma ścieżki, która byłaby możliwa do zmutowania,
                # pozostaw rozwiązanie bez zmian
                mutated_solution = solution
        else:
            # Mutacja nie zaszła, ze względu na związane z nią prawdopodobieństwo
            mutated_solution = solution

        mutated_population.append(mutated_solution)

    return mutated_population


def mutation_2(population: list[Solution], probability: float) -> list[Solution]:
    """
    Mutacja: Zadaniem tego operatora mutacji jest dokonanie mutacji, o ile
    liczba losowana w ramach funkcji reprezentującej ten operator będzie mniejsza
    lub równa wartości prawdopodobieństwa będącego parametrem wejściowym. Obie
    wartości są znormalizowane do przedziału [0,1]. W tym wariancie mutacja polega
    na "zlepieniu" list wierzchołków dla wszystkich samochodów i rozdzieleniu ich w
    dowolnych miejscach. Jedynym ograniczeniem jest sytuacja, gdy po zastosowaniu tej
    operacji jakiś pojazd nie miałby żadnych wierzchołków. Wtedy operator mutacji
    zostaje zastosowany ponownie aż do znalezienia właściwej kombinacji.

    Args:
        population: Lista osobników powstałych w wyniku zajścia operatora krzyżowania
        probability: Prawdopodobieństwo zajścia mutacji znormalizowana do przedziału [0,1]

    Returns:
        Lista osobników po zajściu mutacji. Mutacja mogła nie wystąpić i w takim wypadku
        dany osobnik nie ulega modyfikacji.

    """
    mutated_population = []
    for solution in population:
        # Sprawdzenie, czy mutacja wystąpi
        if random.random() <= probability:
            # Usuń 0 z list i wylosuj ich kolejność
            routes_list = [route[1:-1] for route in solution.routes.values()]
            random.shuffle(routes_list)

            # Zmień listę list na listę wszystkich wierzchołków zgodnie z wylosowaną kolejnością
            all_vertices = [vertex for route in routes_list for vertex in route]

            # Sprawdzenie liczby pojazdów
            num_routes = len(solution.routes)

            # Ustalenie miejsc podziału w celu wyznaczenia nowych ścieżek
            if num_routes > 1:
                split_points = sorted(random.sample(range(1, len(all_vertices)), num_routes - 1))
            else:
                split_points = []

            # Podział listy zgodnie z ustalonymi punktami podziału
            new_routes = [all_vertices[i:j] for i, j in zip([0] + split_points, split_points + [None])]

            # Dodanie 0 na powrót w celu utworzenia pełnych rozwiązań
            mutated_routes = {vehicle: [0] + route + [0] for vehicle, route in enumerate(new_routes, start=1)}
            mutated_solution = Solution(mutated_routes)
        else:
            # Mutacja nie zaszła, ze względu na związane z nią prawdopodobieństwo
            mutated_solution = solution

        mutated_population.append(mutated_solution)

    return mutated_population
