from app.classes.solution import Solution
import random


def crossover(population: list[(Solution, Solution)]) -> list[Solution]:
    """
    Operator krzyżowania:
    Ma za zadanie skrzyżować ze sobą wyselekcjonowane osobniki, tak aby
    powstało nowe pokolenie. Krzyżowanie działa na zasadzie wyboru wierzchołków
    w kolejności ich występowania. To znaczy, że jeśli wierzchołek o danym numerze
    pojawi się po raz pierwszy, to jest brany pod uwagę, a drugie wystąpienie jest
    wykreślane. Jeśli wystąpi zbyt mała / zbyt duża liczba pojazdów są one odpowiednio
    dodawane / rozdzielane-liczba pojazdów pozostaje stała dla każdego osobnika.
    Należy też pamiętać o wykreśleniu 0 na początku i końcu listy wierzchołków
    przypisanej do każdego pojazdu.

    Args:
        population: Lista krotek z osobnikami, będących w istocie słownikiem z numerami
        identyfikacyjnymi samochodów i ich ścieżkami. Ponieważ operator krzyżowania może
        zmienić czas przejazdu będący określeniem jakości danego rozwiązania, nie ma potrzeby
        wykorzystania tej danej w ramach procesu krzyżowania. Czas zostanie obliczony ponownie
        dopiero po zastosowaniu operatora mutacji.

    Returns:
        Lista osobników powstałych w wyniku przeprowadzenia krzyżowania, wraz z zaktualizowanym
        czasem.

    """
    offspring = []

    for parent1, parent2 in population:
        # Dodanie do siebie rodziców na razie bez zmiany kolejności list
        combined_routes = []
        for vehicle_id in parent1.routes:
            combined_routes.append(parent1.routes[vehicle_id][1:-1])  # Usunięcie 0 z rodzica 1
        for vehicle_id in parent2.routes:
            combined_routes.append(parent2.routes[vehicle_id][1:-1])  # Usunięcie 0 z rodzica 2

        # Przemieszanie list
        random.shuffle(combined_routes)

        # Utworzenie nowego rozwiązania
        new_routes = {}
        seen_vertices = set()
        vehicle_id = 1
        for route in combined_routes:
            new_route = []
            for vertex in route:
                if vertex not in seen_vertices:
                    new_route.append(vertex)
                    seen_vertices.add(vertex)
            if new_route:  # Usunięcie pustych list
                new_routes[vehicle_id] = new_route
                vehicle_id += 1

        # Dostosowanie liczby pojazdów (list)
        original_num_vehicles = len(parent1.routes)

        # Gdy pojazdów jest za dużo
        while len(new_routes) > original_num_vehicles:
            route_to_distribute = random.choice(list(new_routes.keys()))
            vertices_to_distribute = new_routes.pop(route_to_distribute)
            for vertex in vertices_to_distribute:
                target_route = random.choice(list(new_routes.keys()))
                insert_index = random.randint(0, len(new_routes[target_route]))
                new_routes[target_route].insert(insert_index, vertex)

        # Gdy pojazdów jest za mało
        while len(new_routes) < original_num_vehicles:
            splittable_routes = [route_id for route_id, route in new_routes.items() if len(route) > 1]
            route_to_split = random.choice(splittable_routes)
            split_index = random.randint(1, len(new_routes[route_to_split]) - 1)
            new_routes[vehicle_id] = new_routes[route_to_split][split_index:]
            new_routes[route_to_split] = new_routes[route_to_split][:split_index]
            vehicle_id += 1

        # Create a new Solution object with the new routes for each offspring
        offspring_solution = Solution(
            routes={vehicle_id: [0] + route + [0] for vehicle_id, route in new_routes.items()})
        offspring.append(offspring_solution)

    return offspring
