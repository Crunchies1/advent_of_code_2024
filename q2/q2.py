from helpers.helpers import parse_input_file_nested_lists

def main():
    reports = parse_input_file_nested_lists("q2/input.txt")
    print(total_safe_reports(reports))

def total_safe_reports(reports: list[list[int]]) -> int:
    print(len(reports))
    return sum(report_safe_dampener(report) for report in reports)

# It's brute force, but call report safe on all reports with one level removed at a time
def report_safe_dampener(report: list[int]) -> int:
    for idx in range(len(report)):
        new_report = report[:idx] + report[idx+1:]
        if report_safe(new_report):
            return True
    return False

def report_safe(levels: list[int]) -> bool:
    if len(levels) < 2:
        return True
    
    # Set decreasing and last levels
    decreasing = False
    last_level = levels[1]
    total_diff = abs(levels[1] - levels[0])
    if total_diff > 3 or total_diff < 1:
        return False
    if levels[0] > last_level:
        decreasing = True

    for level in levels[2:]:
        # Check if the difference is within the allowed range
        diff = abs(level - last_level)
        if diff > 3 or diff < 1:
            return False
        # Check if the levels are consistently decreasing or increasing
        if decreasing and level > last_level or not decreasing and level < last_level:
            return False
        last_level = level
    return True

main()
