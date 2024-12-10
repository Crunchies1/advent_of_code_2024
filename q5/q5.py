from helpers.helpers import parse_input_hashmap, parse_input_file_nested_lists

def main():
    updates = parse_input_file_nested_lists('q5/updates.txt', ',')
    print(add_middle_for_updates_ordered_correctly(updates))

def update_ordered_correctly(hashmap: dict[int, int], update: list[int]) -> bool:
    pages = set() 
    for i in range(len(update)):
        pages.add(update[i]) # This is fine because pages don't have dependencies on themselves

        # Ignore elements that don't have a rule associated
        if update[i] not in hashmap:
            continue 

        # Check that the elements are in the correct order
        dependent_pages = hashmap.get(update[i])
        for page in dependent_pages:
            if page not in pages:
                return False
        
    return True

def corrected_update(hashmap: dict[int, list[int]], update: list[int]) -> list[int]:
    correct_update = []
    while hashmap:
        deleted_entries = set()
        for entry in hashmap:
            if hashmap[entry] == []:
                correct_update.append(entry)
                deleted_entries.add(entry)

        for entry in hashmap:
            for deleted_entry in deleted_entries:
                if deleted_entry in hashmap[entry]:
                    hashmap[entry].remove(deleted_entry)

        for deleted_entry in deleted_entries:
            del hashmap[deleted_entry]

    return correct_update

def add_middle_for_updates_ordered_correctly(updates: list[list[int]]) -> int:
    already_correct_middle_count = 0
    corrected_middle_count = 0
    for update in updates:
        hashmap = parse_input_hashmap('q5/orderings.txt', update)
        if update_ordered_correctly(hashmap, update):
            middle_number = update[len(update) // 2]
            already_correct_middle_count += middle_number
        else:
            correct_update = corrected_update(hashmap, update)
            corrected_middle_count += correct_update[len(correct_update) // 2]

    print(corrected_middle_count)
    return already_correct_middle_count

main()
