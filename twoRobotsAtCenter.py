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

    center = int(width/2), int(height/2)
    robot1 = robot2 = center

    time_elapsed = angle_of_robot2 = 0

    exit_to_disk, angle_of_exit = random_exit(radius, center)

    state = "move towards the perimeter"
     
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(white)

        if state == "evacuate the last robot (robot1)" or state == "evacuate the last robot (robot2)":
            if state == "evacuate the last robot (robot1)":
                robot1 = move_in_straight_line(robot1, speed_in_a_straight_line, "right")
            if state == "evacuate the last robot (robot2)":
                robot2 = move_in_straight_line(robot2, speed_in_a_straight_line, "left")
            time_elapsed += speed_along_perimeter
            time_elapsed = round(time_elapsed, 5)
            if time_elapsed >= 1 + angle_of_exit + (2 * math.sin(angle_of_exit)):
                time_elapsed = 1 + angle_of_exit + (2 * math.sin(angle_of_exit))
                state = "evacuated"

        elif state == "move towards the perimeter":
            robot1 = move_in_straight_line(robot1, speed_in_a_straight_line, "up")
            robot2 = move_in_straight_line(robot2, speed_in_a_straight_line, "up")
            time_elapsed += speed_along_perimeter
            time_elapsed = round(time_elapsed, 5)
            if distance(robot1, center) >= radius:
                state = "move along the perimeter"

        elif state == "move along the perimeter": 
            if angle_of_robot2 >= angle_of_exit or (-angle_of_robot2 + math.pi * 2) <= angle_of_exit:
                if angle_of_robot2 >= angle_of_exit:
                    state = "evacuate the last robot (robot1)"
                else:
                    angle_of_exit = 2 * math.pi - angle_of_exit
                    state = "evacuate the last robot (robot2)"

                time_elapsed = 1 + angle_of_exit
            else:
                angle_of_robot2 += speed_along_perimeter

                time_elapsed += speed_along_perimeter
                time_elapsed = round(time_elapsed, 5)

            robot1 = move_along_perimeter(-angle_of_robot2, radius, center)
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
            robot1 = robot2 = center
            exit_to_disk, angle_of_exit = random_exit(radius, center)
            state = "move towards the perimeter"

     
    pygame.quit()
 
if __name__ == '__main__':
    main()