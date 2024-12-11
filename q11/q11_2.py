from helpers.helpers import parse_input_file_list
from collections import defaultdict

def main():
    stone_list: list[int] = parse_input_file_list("q11/input.txt")
    # This essentially records the number of stones produced from a single
    # digit starting point after a certain number of evolutions
    stone_memo: dict[int, list[int]] = defaultdict(list)
    prebuilt_memo: dict[int, list[int]] = parse_file_memo()
    total_extra_stones: int = 0
    
    for _ in range(30):
        stone_list = evolve_stones(stone_list, stone_memo)
        print(len(stone_list))

    for blink in range(45):
        stone_list, extra_stones = evolve_stones_refined(stone_list, stone_memo, prebuilt_memo, 30 + blink)
        total_extra_stones += extra_stones
        print(f"blink {blink}: {len(stone_list) + total_extra_stones}")

    print(len(stone_list) + total_extra_stones)

def evolve_stones(stone_list: list[int], stone_memo: dict[int, list[int]]) -> list[int]:
    new_stone_list: list[int] = []
    for stone_idx in range(len(stone_list)):
        # Check if stone has been evolved before, if so we use that
        stone = stone_list[stone_idx]
        if stone in stone_memo:
            new_stone_list.extend(stone_memo[stone])
            continue

        # Evolve the stone and record it in the memo
        if stone == 0:
            new_stone_list.append(1)
            stone_memo[stone] = [1]
        elif len(str(stone)) % 2 == 0:
            left_val = int(str(stone)[:len(str(stone))//2])
            right_val = int(str(stone)[len(str(stone))//2:])
            new_stone_list.append(left_val)
            new_stone_list.append(right_val)
            stone_memo[stone] = [left_val, right_val]
        else:
            next_val = stone * 2024
            new_stone_list.append(next_val)
            stone_memo[stone] = [next_val]

    return new_stone_list

def evolve_stones_refined(stone_list: list[int], stone_memo: dict[int, list[int]], prebuilt_memo: dict[int, list[int]], blink_num: int) -> tuple[list[int], int]:
    new_stone_list: list[int] = evolve_stones(stone_list, stone_memo)
    extra_stones: int = 0

    to_remove: set[int] = set()
    for stone in new_stone_list:
        if stone in prebuilt_memo:
            to_remove.add(stone)
            extra_stones += prebuilt_memo[stone][74 - blink_num]

    return [stone for stone in new_stone_list if stone not in to_remove], extra_stones


# Dirty function to pregenerate the memo
def write_half_to_file_memo(total: int):
    file = open("q11/stone_memo.txt", "w")
    stone_memo: dict[int, list[int]] = defaultdict(list)
    for i in range(10):
        file.write(f"{i}|")
        stone_list: list[int] = [i]
        for i in range(total):
            stone_list = evolve_stones(stone_list, stone_memo)
            if i == total - 1:
                file.write(f"{len(stone_list)}")
            else:
                file.write(f"{len(stone_list)} ")
        file.write("\n")


def parse_file_memo() -> dict[int, list[int]]:
    file = open("q11/stone_memo.txt", "r")
    num_stone_memo: dict[int, list[int]] = {}
    for line in file:
        line = line.strip().split("|")
        stone = int(line[0])
        num_stone_memo[stone] = list(map(int, line[1].split()))
    return num_stone_memo

# write_half_to_file_memo(45)
main()