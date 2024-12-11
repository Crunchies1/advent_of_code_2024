from collections import defaultdict

def parse_input_file_list(file_path):
    with open(file_path, "r") as file:
        return [int(line) for line in file.read().split(" ")]

def parse_input_file_two_vertical_lists(file_path):
    list1 = []
    list2 = []

    with open(file_path, 'r') as file:
        for line in file:
            # Split the line into two values
            value1, value2 = line.split()
            # Convert the values to integers and append to the respective lists
            list1.append(int(value1))
            list2.append(int(value2))

    return list1, list2

def parse_input_file_nested_lists(file_path, separator=' '):
    with open(file_path, 'r') as f:
        # Read lines, split by whitespace, and convert to integers
        return [[int(num) for num in line.strip().split(separator)] for line in f]
    
def parse_input_file_single_string(file_path):
    with open(file_path, 'r') as f:
        return f.read()
    
def parse_input_file_2d_array(file_path):
    with open(file_path, 'r') as file:
        # Read all lines and strip whitespace
        lines = [line.strip() for line in file.readlines()]
        # Filter out empty lines
        lines = [line for line in lines if line]
        # Convert each line into a list of characters
        grid = [list(line) for line in lines]
    return grid

def parse_input_hashmap(file_path, accepted_ints: list[int]):
    hashmap = defaultdict(list)
    with open(file_path, 'r') as f:
        for line in f:
            split = line.split('|')
            if int(split[1]) in accepted_ints and int(split[0]) in accepted_ints:
                hashmap[int(split[1])].append(int(split[0]))
                
    for accepted_int in accepted_ints:
        if accepted_int not in hashmap:
            hashmap[accepted_int] = []
    return hashmap

def parse_input_file_q7(file_path) -> list[tuple[int, list[int]]]:
    lines = []
    with open(file_path, 'r') as f:
        for line in f:
            split = line.split(' ')
            total_number = int(split[0][:-1])
            numbers = [int(num) for num in split[1:]]
            lines.append((total_number, numbers))
    return lines
    