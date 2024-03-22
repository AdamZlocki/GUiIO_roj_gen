from app.classes.vehicle import Vehicle
from typing import Dict, List
import random

def dispersal(probability, actual_cockroach: Dict[Vehicle, List[int]], vehicle_order: List[Vehicle]):
    """Wywołanie rozproszenia z zadanym prawdopodobieństwem - Z każdego samochodu bierzemy losowe miasto i zamieniamy je z innym losowym samochodem"""
    generated_number = random.uniform(0, 0.99)
    if generated_number < probability:
        moved_elem = set()
        # lst_of_vehicle_which_get_new_elem = set()
        for vehicle in vehicle_order:
            cockroach_data = actual_cockroach[vehicle]

            random_index = random.randint(0, len(cockroach_data) - 1)
            random_element = cockroach_data[random_index]

            # Element który już raz został przeniesiony nie może zostać przeniesiony ponownie.
            while random_element in moved_elem:
                random_index = random.randint(0, len(cockroach_data) - 1)
                random_element = cockroach_data[random_index]

            moved_elem.add(random_element)

            other_vehicle = random.choice([v for v in vehicle_order if v != vehicle])
            # Do wyjebania raczej
            # Sprawdzanie czy wylosowany samochód dostał już jakiś element - Zabezpieczenie przed zmienieniem długości rozwiązań dla każdego samochodu
            # while other_vehicle in lst_of_vehicle_which_get_new_elem:
            #     other_vehicle = random.choice([v for v in vehicle_order if v != vehicle])
            #
            # lst_of_vehicle_which_get_new_elem.add(other_vehicle)

            other_index = random.randint(0, len(actual_cockroach[other_vehicle]) - 1)

            actual_cockroach[vehicle].remove(random_element)
            actual_cockroach[other_vehicle].insert(other_index, random_element)

        return actual_cockroach
    else:
        return actual_cockroach
