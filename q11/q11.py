from helpers.helpers import parse_input_file_list

class LinkedStone:
    def __init__(self, value: int):
        self.value = value
        self.next = None

    def evolve(self) -> int:
        if self.value == 0:
            return self.set_one()
        elif len(str(self.value)) % 2 == 0:
            return self.split()
        else:
            return self.multiply()

    def set_one(self) -> int:
        self.value = 1
        return 0

    def split(self) -> int:
        string_val = str(self.value)
        right = int(string_val[len(string_val)//2:])
        left = int(string_val[:len(string_val)//2])
        self.value = left
        new_stone = LinkedStone(right)
        if self.next: # Replace next stone with this one
            next_stone = self.next
            new_stone.next = next_stone
        self.next = new_stone
        return 1

    def multiply(self) -> int:
        self.value *= 2024
        return 2

def main():
    stone_list: list[int] = parse_input_file_list("q11/input.txt")
    head: LinkedStone = LinkedStone(stone_list[0])
    cur_stone: LinkedStone = head
    for stone in stone_list[1:]:
        new_stone = LinkedStone(stone)
        cur_stone.next = new_stone
        cur_stone = new_stone

    for _ in range(35):
        print(evolve_stones(head))

def evolve_stones(head_stone: LinkedStone) -> int:
    total_stones: int = 0
    cur_stone: LinkedStone | None = head_stone

    while cur_stone:
        if cur_stone.evolve() == 1:
            cur_stone = cur_stone.next.next
            total_stones += 2
            continue
        
        cur_stone = cur_stone.next
        total_stones += 1
    return total_stones

main()