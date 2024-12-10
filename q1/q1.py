from helpers.helpers import parse_input_file_two_vertical_lists

def main():
    locations_1, locations_2 = parse_input_file_two_vertical_lists("q1/input.txt")
    print(differences(locations_1, locations_2))
    print(similarities(locations_1, locations_2))

def differences(locations_1: list[int], locations_2: list[int]) -> int:
    locations_1.sort()
    locations_2.sort()

    return sum_adjacents(locations_1, locations_2)

def sum_adjacents(locations_1: list[int], locations_2: list[int]) -> int:
    sum: int = 0
    for idx in range(len(locations_1)):
        sum += abs(locations_1[idx] - locations_2[idx])
    return sum

def similarities(locations_1: list[int], locations_2: list[int]) -> int:
    similarities: dict[int, int] = {}
    total_similarities: int = 0
    for location_1 in locations_1:
        if location_1 in similarities:
            total_similarities += similarities[location_1]
            continue

        same_occurences: int = 0
        for location_2 in locations_2:
            if location_1 == location_2:
                same_occurences += 1

        similarities[location_1] = same_occurences * location_1
        total_similarities += similarities[location_1]

    return total_similarities

main()
