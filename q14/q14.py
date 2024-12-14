import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Global variables to control the animation
current_index = 0
positions_list = []

def parse_input_file(file_path: str) -> list[tuple[list[int]]]:
    with open(file_path, "r") as file:
        return [parse_robot_line(line) for line in file]

# p=82,54 v=14,-84
def parse_robot_line(line: str) -> tuple[list[int]]:
    str_pos, str_vel = line.split(" ")
    position = list(map(int, str_pos[2:].split(",")))
    velocity = list(map(int, str_vel[2:].split(",")))
    return position, velocity

def update_robots(robots: list[tuple[list[int]]]) -> list[tuple[list[int]]]:
    new_robots = []
    for robot in robots:
        robot = move_robot(robot)
        new_robots.append(robot)
    return new_robots

def move_robot(robot: tuple[list[int]]) -> tuple[list[int]]:
    position, velocity = robot
    new_position = [position[0] + velocity[0], position[1] + velocity[1]]
    if new_position[0] < 0:
        while new_position[0] < 0:
            new_position[0] = 101 + new_position[0]
    if new_position[1] < 0:
        while new_position[1] < 0:
            new_position[1] = 103 + new_position[1]
    if new_position[0] >= 101:
        while new_position[0] >= 101:
            new_position[0] = new_position[0] - 101
    if new_position[1] >= 103:
        while new_position[1] >= 103:
            new_position[1] = new_position[1] - 103
    return new_position, velocity

def calculate_quadrant_scores(robots: list[tuple[list[int]]]) -> int:
    quadrants = {1: 0, 2: 0, 3: 0, 4: 0}
    for position, _ in robots:
        if position[0] < 50 and position[1] < 51:
            quadrants[1] += 1
        elif position[0] < 50 and position[1] > 51:
            quadrants[2] += 1
        elif position[0] > 50 and position[1] < 51:
            quadrants[3] += 1
        elif position[0] > 50 and position[1] > 51:
            quadrants[4] += 1
    print(quadrants)
    return quadrants[1] * quadrants[2] * quadrants[3] * quadrants[4]

def generate_positions(robots: list[tuple[list[int], list[int]]], steps: int) -> list[list[tuple[list[int], list[int]]]]:
    positions = []
    for _ in range(steps):
        robots = [move_robot(robot) for robot in robots]
        positions.append([robot[0] for robot in robots])
    return positions

def update_plot(scatter, time_text):
    global current_index, positions_list
    scatter.set_offsets(positions_list[current_index])
    time_text.set_text(f'Elapsed time: {current_index} s')
    plt.draw()

def next_step(event, scatter, time_text):
    global current_index
    if current_index < len(positions_list) - 1:
        current_index += 1
        update_plot(scatter, time_text)

def prev_step(event, scatter, time_text):
    global current_index
    if current_index > 0:
        current_index -= 1
        update_plot(scatter, time_text)


def next_step_100(event, scatter, time_text):
    global current_index
    if current_index < len(positions_list) - 1:
        current_index += 100
        update_plot(scatter, time_text)

def prev_step_100(event, scatter, time_text):
    global current_index
    if current_index > 0:
        current_index -= 100
        update_plot(scatter, time_text)

def main():
    global current_index, positions_list
    current_index = 0

    robots = parse_input_file("q14/input.txt")
    positions_list = generate_positions(robots, 10000)

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)
    ax.set_xlim(0, 101)
    ax.set_ylim(0, 103)
    scatter = ax.scatter([], [])
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

    update_plot(scatter, time_text)

    ax_next = plt.axes([0.81, 0.05, 0.1, 0.075])
    ax_prev = plt.axes([0.7, 0.05, 0.1, 0.075])
    ax_next_100 = plt.axes([0.48, 0.05, 0.1, 0.075])
    ax_prev_100 = plt.axes([0.59, 0.05, 0.1, 0.075])

    btn_next = Button(ax_next, 'Next')
    btn_prev = Button(ax_prev, 'Prev')
    btn_next_100 = Button(ax_next_100, 'Next_100')
    btn_prev_100 = Button(ax_prev_100, 'Prev_100')

    btn_next.on_clicked(lambda event: next_step(event, scatter, time_text))
    btn_prev.on_clicked(lambda event: prev_step(event, scatter, time_text))
    btn_next_100.on_clicked(lambda event: next_step_100(event, scatter, time_text))
    btn_prev_100.on_clicked(lambda event: prev_step_100(event, scatter, time_text))

    plt.show()

main()