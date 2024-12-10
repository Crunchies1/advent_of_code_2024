import math
from helpers.helpers import parse_input_file_single_string
from collections import defaultdict

# The test input answer is 1184151

def main():
    input_string: str = parse_input_file_single_string('q9/input.txt')
    disk: list[str] = list(input_string)
    print(disk_partition_part_two(disk))

# Solution for part one
# Strings are in the form of size, empty, size, empty, ...
def disk_partition(disk: list[str]) -> int:
    total_checksum: int = 0

    # Use a two pointer approach to find the total checksum, without modifying anything
    # The left pointer will be tracking the leftmost EMPTY space,
    # The right pointer will be tracking the rightmost USED space
    left_pointer: int = 0
    right_pointer: int = len(disk) - 1
    space_counter: int = 0

    while right_pointer > left_pointer:
        # Add up disk space of used left side
        if left_pointer % 2 == 0 :
            current_key: int = left_pointer // 2
            checksum, space_counter = sum_checksum(disk, current_key, int(disk[left_pointer]), space_counter)
            total_checksum += checksum
            left_pointer += 1
            continue 

        # Move used disk space from the right side to the left side
        # We have three cases, one where we can fill a historic space
        # One where we can fill a space with a contiguous block of data
        # One where we can't fill anything
        space_left: int = int(disk[left_pointer])
        data_to_be_moved: int = int(disk[right_pointer])
        current_key: int = right_pointer // 2

        # Check the history first to see if we can fill a historic space
        if space_left > data_to_be_moved:
            checksum, space_counter = sum_checksum(disk, current_key, data_to_be_moved, space_counter)
            total_checksum += checksum

            disk[left_pointer] = str(space_left - data_to_be_moved)
            right_pointer -= 2 # move right pointer to next data index

        elif space_left < data_to_be_moved:
            checksum, space_counter = sum_checksum(disk, current_key, space_left, space_counter)
            total_checksum += checksum

            disk[right_pointer] = str(data_to_be_moved - space_left)
            left_pointer += 1 # Move left pointer to next data index

        else:
            checksum, space_counter = sum_checksum(disk, current_key, space_left, space_counter)
            total_checksum += checksum

            left_pointer += 1
            right_pointer -= 2

    # Add up the last bits of data
    current_key: int = left_pointer // 2
    checksum, _ = sum_checksum(disk, current_key, int(disk[left_pointer]), space_counter)
    total_checksum += checksum

    return total_checksum

def sum_checksum(disk: str, current_key: int, space_used: int, space_counter: int) -> tuple[int, int]:
    checksum: int = 0
    while space_used:
        checksum += current_key * space_counter
        space_used -= 1
        space_counter += 1

    return checksum, space_counter


def disk_partition_part_two(disk: list[str]) -> int:
    total_checksum: int = 0
    space_counter, history = generate_space_history(disk)

    # We want to iterate from the right to the left, making sure we fill in the 
    # space history. We only need to try moving data once.
    right_pointer: int = len(disk) - 1
    while right_pointer >= 0:
        current_key: int = right_pointer // 2
        data_to_be_moved: int = int(disk[right_pointer])
        # Check if we can fill a historic space
        checksum: int = check_history(history, data_to_be_moved, current_key)
        if checksum:
            total_checksum += checksum
            space_counter -= data_to_be_moved

        else: 
            for _ in range(data_to_be_moved):
                total_checksum += current_key * space_counter
                space_counter -= 1

        right_pointer -= 1
        space_counter -= int(disk[right_pointer])
        right_pointer -= 1
        purge_history(history, space_counter)

    return total_checksum

# I'm fine with doing this because the max space is 9, but crap man this sucks
def check_history(history: dict[int, list[int]], data_to_be_moved: int, current_key: int) -> int:
    checksum: int = 0
    smallest_index: int = math.inf
    smallest_index_space: int = 0
    cur_space_check: int = data_to_be_moved

    while cur_space_check <= 9:
        if len(history[cur_space_check]) > 0:
            smallest_index = min(smallest_index, history[cur_space_check][0])
            if smallest_index == history[cur_space_check][0]:
                smallest_index_space = cur_space_check
        cur_space_check += 1

    if smallest_index_space:
        index: int = history[smallest_index_space].pop(0)
        while data_to_be_moved:
            checksum += current_key * index
            smallest_index_space -= 1
            data_to_be_moved -= 1
            index += 1

        if smallest_index_space > 0:
            history[smallest_index_space].append(index)
            history[smallest_index_space].sort()

    return checksum

# Remove all indices that are greater than the right pointer 
def purge_history(history: dict[int, list[int]], space_counter: int) -> None:
    for space, indices in history.items():
        for index in indices:
            if index > space_counter:
                history[space].remove(index)


def generate_space_history(disk: list[str]) -> tuple[int, dict[int, list[int]]]:
    history: dict[int, list[int]] = defaultdict(list)
    total_space: int = 0

    for index in range(len(disk)):
        space_left: int = int(disk[index])
        if index % 2 == 1 and space_left > 0:
            history[space_left].append(total_space)
            history[space_left].sort()
        total_space += space_left

    return total_space - 1, history

main()
