import math
import random
import numpy as np
import scipy.stats


def mean_confidence_interval(data, confidence=0.99):#taken from https://stackoverflow.com/questions/15033511/compute-a-confidence-interval-from-sample-data
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h, h

def distance(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def distance_from_perimeter():
    random_x = 1
    random_y = 1
    while distance((random_x, random_y), (0,0)) > 1:
        random_x = (random.random() * 2) - 1
        random_y = (random.random() * 2) - 1

    return 1 - distance((random_x, random_y), (0,0))

number_of_tests = 100000

data = []

for i in range(1, number_of_tests+1):
    angle_of_exit = random.random() * math.pi * 2
    if angle_of_exit > math.pi:
        angle_of_exit = angle_of_exit - math.pi
    time_to_evacuate = distance_from_perimeter() + angle_of_exit + (2 * math.sin(angle_of_exit))
    data.append(time_to_evacuate)

confidence_interval = mean_confidence_interval(data, 0.95)
print("Expected runtime: " + str(confidence_interval[0]) + " +/- " + str(confidence_interval[3]))