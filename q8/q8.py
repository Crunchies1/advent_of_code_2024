#  For each pair of antennas, there are two antinodes that occur.
#  So if there is an antenna at coord (3, 4) and another at (5, 7),
#  there will be an antinode at (1, 1) and another at (7, 10).
#
#  We can take the difference between the x-coordinates and the y-coordinates
#  and then add that difference to the larger coordinate and subtract it from
#  the smaller coordinate to get the two antinodes.
#
#  We can do this for all pairs of antennas and sum up the number of unique
#  antinodes to get the total number of antinodes.

from helpers.helpers import parse_input_file_2d_array
from collections import defaultdict

def main():
    antenna_map = parse_input_file_2d_array("q8/input.txt")
    print(find_all_antinodes(antenna_map))

def find_all_antinodes(antenna_map: list[list[str]]) -> int:
    antenna_dict: dict[str, tuple[int, int]] = defaultdict(list)
    antinodes: set[tuple[int, int]] = set()

    # Record coordinates of all antennas grouped by letter/number
    for row_idx, row in enumerate(antenna_map):
        for col_idx, col in enumerate(row):
            if col != '.':
                antenna_dict[col].append((row_idx, col_idx))

    # For each pair of same-key antennas, find all antinodes
    for antenna_group in antenna_dict.values():
        for antenna_idx in range(len(antenna_group)):
            for other_antenna_idx in range(antenna_idx + 1, len(antenna_group)):
                antinodes.update(get_antinodes(antenna_map, antenna_group[antenna_idx], antenna_group[other_antenna_idx]))

    return len(antinodes)

# Given two antennas, return a list of available antinodes.
def get_antinodes(antenna_map: list[list[str]], antenna_1: tuple[int, int], antenna_2: tuple[int, int]) -> list[tuple[int, int]]:
    antinodes: list[tuple[int, int]] = [antenna_1, antenna_2]

    row_diff: int = antenna_2[0] - antenna_1[0]
    col_diff: int = antenna_2[1] - antenna_1[1]

    cur_row_idx: int = antenna_1[0]
    cur_col_idx: int = antenna_1[1]
    while 0 <= (cur_row_idx - row_diff) < len(antenna_map) and 0 <= (cur_col_idx - col_diff) < len(antenna_map[0]):
        cur_row_idx -= row_diff
        cur_col_idx -= col_diff
        new_antenna: tuple[int, int] = (cur_row_idx, cur_col_idx)
        antinodes.append(new_antenna)

    cur_row_idx: int = antenna_2[0]
    cur_col_idx: int = antenna_2[1]
    while 0 <= (cur_row_idx + row_diff) < len(antenna_map) and 0 <= (cur_col_idx + col_diff) < len(antenna_map[0]):
        cur_row_idx += row_diff
        cur_col_idx += col_diff
        new_antenna: tuple[int, int] = (cur_row_idx, cur_col_idx)
        antinodes.append(new_antenna)

    return antinodes

main()