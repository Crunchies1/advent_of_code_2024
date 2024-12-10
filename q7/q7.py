from helpers.helpers import parse_input_file_q7

def main():
    equations: list[tuple[int, list[int]]] = parse_input_file_q7('q7/input.txt')
    total_sum: int = 0
    for target, numbers in equations:
        if is_equation_solvable(target, numbers):
            total_sum += target

    print(total_sum)

def is_equation_solvable(target: int, numbers: list[int]) -> bool:
    def solver(num_idx: int, total: int) -> bool:
        if total > target:
            return False
        
        if num_idx == len(numbers):
            return target == total
    
        if solver(num_idx+1, total + numbers[num_idx]) or \
            solver(num_idx+1, total * numbers[num_idx]) or \
            solver(num_idx+1, combine_numbers(total, numbers[num_idx])):
            return True

        return False

    return solver(1, numbers[0])

def combine_numbers(left_number: int, right_number: int) -> int:
    string_number = str(left_number) + str(right_number)
    return int(string_number)

main()