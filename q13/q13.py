import sympy as sym

# Button A: X+55, Y+84
# Button B: X+64, Y+29
# Prize: X=6049, Y=5045
def parse_input_file_q13(file_path) -> tuple[int, list[int]]:
    machines: list[list[tuple[int, int]]] = []
    with open(file_path, 'r') as f:
        not_end: bool = True
        while not_end:
            machine: list[tuple[int, int]] = []
            for _ in range(3):
                line = f.readline().strip()
                machine.append(parse_button_or_prize_line(line))
            if f.readline() == "":
                not_end = False
            machines.append(machine)
    return machines

def parse_button_or_prize_line(line: str) -> tuple[int, int]:
    x_y_changes = line.split(": ")[1]
    split = x_y_changes.split(", ")
    x_value: int = int(split[0][2:])
    y_value: int = int(split[1][2:])
    return x_value, y_value

def main():
    machines: list[list[tuple[int, int]]] = parse_input_file_q13("q13/input.txt")
    total_tokens: int = 0
    for machine in machines:
        total_tokens += cheapest_win_prize_2(machine)
    print(total_tokens)

def cheapest_win_prize(machine: list[tuple[int, int]]) -> int:
    button_a_change, button_b_change, prize = machine
    visited: dict[tuple[int, int], int] = dict()

    def dfs(coordinate: tuple[int, int], cost: int) -> None:
        x, y = coordinate
        visited[coordinate] = min(visited.get(coordinate, float("inf")), cost)

        x_delta, y_delta = button_a_change
        new_x: int = x + x_delta
        new_y: int = y + y_delta
        if (new_x, new_y) not in visited and new_x <= prize[0] and new_y <= prize[1]:
            dfs((new_x, new_y), cost + 3)

        x_delta, y_delta = button_b_change
        new_x: int = x + x_delta
        new_y: int = y + y_delta
        if (new_x, new_y) not in visited and new_x <= prize[0] and new_y <= prize[1]:
            dfs((new_x, new_y), cost + 1)

    dfs((0, 0), 0)

    if prize in visited:
        return visited[prize]
    
    return 0

# Essentially the problem we want to solve is:
# z = ax + by
# z = cx + dy
def cheapest_win_prize_2(machine: list[tuple[int, int]]) -> int:
    button_a_change, button_b_change, prize = machine
    prize = (prize[0] + 10000000000000, prize[1] + 10000000000000)
    
    x,y = sym.symbols('x,y')
    eq1 = sym.Eq(button_a_change[0] * x + button_b_change[0] * y, prize[0])
    eq2 = sym.Eq(button_a_change[1] * x + button_b_change[1] * y, prize[1])
    result = sym.solve([eq1, eq2], (x, y))
    x_val, y_val = result[x], result[y]
    if x_val < 0 or y_val < 0:
        return 0
    if type(x_val) == sym.core.numbers.Integer and type(y_val) == sym.core.numbers.Integer:
        return 3 * x_val + y_val 
    return 0

main()