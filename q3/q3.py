from helpers.helpers import parse_input_file_single_string

def main():
    input = parse_input_file_single_string("q3/input.txt")
    print(scan_for_mul(input))

def scan_for_mul(input: str) -> int:
    total_mul: int = 0
    do = True
    
    while input:
        # Skip if the string does not start with "mul("
        if do and input.startswith("mul("):
            # Find the first number in between the mul and comma
            skip = False
            comma_idx = 4
            while input[comma_idx] != ",":
                # Ensure that we have not reached end of string and that the character is a string digit
                if comma_idx >= len(input) or not input[comma_idx].isdigit():
                    skip = True
                    break
                comma_idx += 1
            if skip:
                input = input[1:]
                continue
            first_num = int(input[4:comma_idx])
            
            # Find the next number after the comma and before the closing parenthesis
            closing_idx = comma_idx + 1
            while input[closing_idx] != ")":
                # Ensure that we have not reached end of string and that the character is a string digit
                if closing_idx >= len(input) or not input[closing_idx].isdigit():
                    skip = True
                    break
                closing_idx += 1
            if skip:
                input = input[1:]
                continue
            second_num = int(input[comma_idx+1:closing_idx])

            # Add the product of the two numbers to the total
            total_mul += first_num * second_num
            input = input[closing_idx+1:]
            continue
        
        elif input.startswith("do()"):
            do = True

        elif input.startswith("don't()"):
            do = False

        input = input[1:]

    return total_mul

main()