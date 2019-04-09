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

number_of_tests = 100000

data = []

for i in range(1, number_of_tests+1):
	angle_of_exit = random.random() * math.pi * 2
	if angle_of_exit > math.pi:
		angle_of_exit = angle_of_exit - math.pi
	time_to_evacuate = 1 + angle_of_exit + (2 * math.sin(angle_of_exit))
	data.append(time_to_evacuate)

confidence_interval = mean_confidence_interval(data, 0.95)
print("Expected runtime: " + str(confidence_interval[0]) + " +/- " + str(confidence_interval[3]))