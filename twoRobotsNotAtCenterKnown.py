import pygame
import math
import random

#some code taken from https://python-forum.io/Thread-Moving-an-object-in-a-circular-path

pygame.init()
font = pygame.font.SysFont(None, 25)

#taken from https://stackoverflow.com/questions/20748326/pygame-waiting-the-user-to-keypress-a-key
from pygame.locals import *
def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                return

def text_display(text, color):
    screen_text = font.render(text, True, color)
    return screen_text

def move_along_perimeter(angle, radius, coords):
    return coords[0] + radius * math.sin(angle), coords[1] + radius * math.cos(angle) * -1

def random_exit(radius, center):
    angle = random.random() * math.pi * 2
    return move_along_perimeter(angle, radius, center), angle

def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def move_in_straight_line(current_position, speed, direction):
    if direction == "up":
        return current_position[0], current_position[1] - speed
    if direction == "left":
        return current_position[0] - speed, current_position[1]
    if direction == "right":
        return current_position[0] + speed, current_position[1]
    return 0

def move_in_straight_line_angled(current_position, speed, destination):
    distance_to_destination = distance(current_position, destination)
    if distance_to_destination == 0:
        return current_position
    vector = current_position[0] - destination[0], current_position[1] - destination[1]
    normalized_vector = (vector[0] / distance_to_destination) * speed, (vector[1] / distance_to_destination) * speed
    return current_position[0] - normalized_vector[0], current_position[1] - normalized_vector[1]

def move_in_straight_line_angled_opposite_direction(current_position, speed, destination):
    distance_to_destination = distance(current_position, destination)
    if distance_to_destination == 0:
        return current_position
    vector = current_position[0] - destination[0], current_position[1] - destination[1]
    normalized_vector = (vector[0] / distance_to_destination) * speed, (vector[1] / distance_to_destination) * speed
    return current_position[0] + normalized_vector[0], current_position[1] + normalized_vector[1]

def random_robot_placement(radius_in_pixels, width_of_screen, height_of_screen):
    random_x = 1
    random_y = 1
    while distance((random_x, random_y), (0,0)) > 1:
        random_x = (random.random() * 2) - 1
        random_y = (random.random() * 2) - 1

    return width_of_screen/2 + random_x * radius_in_pixels, height_of_screen/2 + random_y * radius_in_pixels


def main():
    summed_time_to_evacuate = 0
    number_of_tests = 0
    average_time_to_evacuate = 0

    width = 800
    height = 600
    black = (0, 0, 0)
    white = (255, 255, 255)
    pygame.display.set_caption("Two Robots Evacuating a Disk")
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
     
    radius = 250
    speed_along_perimeter = 0.02
    speed_in_a_straight_line = speed_along_perimeter * radius

    time_elapsed = angle_of_robot2 = 0

    center = int(width/2), int(height/2)

    exit_to_disk, angle_of_exit = random_exit(radius, center)

    robot1 = robot2 = random_robot_placement(radius, width, height)

    distance_from_perimeter = 1 - distance(((robot1[0]-center[0])/radius, (robot1[1]-center[1])/radius),(0, 0))

    print(distance_from_perimeter)

    angle_robots_meet_perimeter = math.atan2((robot1[0]-center[0]),-(robot1[1]-center[1])) % (math.pi * 2)


    angle_of_robot1 = angle_of_robot2 = angle_robots_meet_perimeter

    arc_length_travelled_along_perimeter = 0

    state = "move towards the perimeter"
     
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(white)

        if state == "evacuate the last robot (robot1)" or state == "evacuate the last robot (robot2)":
            if state == "evacuate the last robot (robot1)":
                robot1 = move_in_straight_line_angled(robot1, speed_in_a_straight_line, robot2)
            if state == "evacuate the last robot (robot2)":
                robot2 = move_in_straight_line_angled(robot2, speed_in_a_straight_line, robot1)
            time_elapsed += speed_along_perimeter
            time_elapsed = round(time_elapsed, 5)
            if time_elapsed >= distance_from_perimeter + arc_length_travelled_along_perimeter + (2 * math.sin(arc_length_travelled_along_perimeter)):
                time_elapsed = distance_from_perimeter + arc_length_travelled_along_perimeter + (2 * math.sin(arc_length_travelled_along_perimeter))
                state = "evacuated"

        elif state == "move towards the perimeter":
            robot1 = move_in_straight_line_angled_opposite_direction(robot1, speed_in_a_straight_line, center)
            robot2 = move_in_straight_line_angled_opposite_direction(robot2, speed_in_a_straight_line, center)
            time_elapsed += speed_along_perimeter
            time_elapsed = round(time_elapsed, 5)
            if distance(robot1, center) >= radius:
                if (angle_robots_meet_perimeter - angle_of_exit) % (2 * math.pi) <= math.pi:
                    arc_length_travelled_along_perimeter = (angle_robots_meet_perimeter - angle_of_exit) % (2 * math.pi)
                    state = "move along the perimeter (robot1 reaches exit first)"
                elif (angle_robots_meet_perimeter - angle_of_exit) % (2 * math.pi) > math.pi:
                    arc_length_travelled_along_perimeter = (angle_of_exit - angle_robots_meet_perimeter) % (2 * math.pi)
                    state = "move along the perimeter (robot2 reaches exit first)"
                print(state)

        elif state == "move along the perimeter (robot1 reaches exit first)" or state == "move along the perimeter (robot2 reaches exit first)": 
            if state == "move along the perimeter (robot2 reaches exit first)" and time_elapsed >= distance_from_perimeter + arc_length_travelled_along_perimeter:
                state = "evacuate the last robot (robot1)"
                print(state)
                time_elapsed = distance_from_perimeter + arc_length_travelled_along_perimeter
            elif state == "move along the perimeter (robot1 reaches exit first)" and time_elapsed >= distance_from_perimeter + arc_length_travelled_along_perimeter:
                state = "evacuate the last robot (robot2)"
                print(state)
                time_elapsed = distance_from_perimeter + arc_length_travelled_along_perimeter
            else:
                angle_of_robot1 -= speed_along_perimeter
                angle_of_robot2 += speed_along_perimeter

                time_elapsed += speed_along_perimeter
                time_elapsed = round(time_elapsed, 5)

            robot1 = move_along_perimeter(angle_of_robot1, radius, center)
            robot2 = move_along_perimeter(angle_of_robot2, radius, center)


        pygame.draw.circle(screen, black, (int(robot1[0]), int(robot1[1])), 4, 0)
        pygame.draw.circle(screen, black, (int(robot2[0]), int(robot2[1])), 4, 0)
        pygame.draw.circle(screen, black, center, radius, 2)
        pygame.draw.rect(screen, black, (exit_to_disk[0] - 10,exit_to_disk[1] - 10,20,20), 2)
        pygame.draw.rect(screen, white, (exit_to_disk[0]+2 - 10,exit_to_disk[1]+2 - 10,17,17), 0)
        screen.blit(text_display("time to evacuate: " + str(round(time_elapsed, 2)), black), (50, 50))
        if average_time_to_evacuate != 0:
            screen.blit(text_display("average time to evacuate: " + str(round(average_time_to_evacuate, 2)), black), (50, 550))
        pygame.display.flip()
        clock.tick(10)

        if state == "evacuated":
            wait()
            summed_time_to_evacuate = time_elapsed + summed_time_to_evacuate
            number_of_tests = number_of_tests + 1
            average_time_to_evacuate = summed_time_to_evacuate/number_of_tests
            time_elapsed = angle_of_robot2 = 0
            exit_to_disk, angle_of_exit = random_exit(radius, center)
            robot1 = robot2 = random_robot_placement(radius, width, height)
            distance_from_perimeter = 1 - distance(((robot1[0]-center[0])/radius, (robot1[1]-center[1])/radius),(0, 0))
            angle_robots_meet_perimeter = math.atan2((robot1[0]-center[0]),-(robot1[1]-center[1])) % (math.pi * 2)
            angle_of_robot1 = angle_of_robot2 = angle_robots_meet_perimeter
            state = "move towards the perimeter"

     
    pygame.quit()
 
if __name__ == '__main__':
    main()