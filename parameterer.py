import numpy as np
import os

script_dir = os.path.dirname(__file__)

with open(os.path.join(script_dir, 'populations.csv')) as file:
	lines = [line.split() for line in file]

print(lines)

