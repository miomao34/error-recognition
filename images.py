# import numpy as np
# import scipy
# from scipy import misc
# from scipy import ndimage
import statistics
import math
import json
import sys
import os
import matplotlib.pyplot as plt

from recognition_tools import *


# lines_arrays = []

# for image in images:
#     lines_arrays.append(recognition_tools.get_lines(image))


# avg = statistics.mean(row_means)
# print('\n', avg, '\n')


# recognition_tools.get_dominant_color(images[0])

image_structs = []
with open('config2.json', 'r') as config:
    image_structs = json.load(config)
        
for i, image_struct in enumerate(image_structs):
    if i == 225:
        if not os.path.exists(image_struct["folder"]):
            os.mkdir(image_struct["folder"])
        image = load_image(image_struct['filename'])
        lines = get_lines(image, 3)
        for j, line in enumerate(lines):
            line.save(f'{image_struct["folder"]}/{j}.jpg')
            if j == 0:
                letters = get_letters(line, 25)
                for k, letter in enumerate(letters):
                    letter.save(f'{image_struct["folder"]}/letter_{k:04}.jpg')


alphabet = load_image('alphabet.jpg')
lines = get_lines(alphabet, 3)
letters = []
for line in lines:
    for letter in get_letters(line, 30):
        letters.append(letter)

if not os.path.exists('generated_examples_output/alphabet'):
    os.mkdir('generated_examples_output/alphabet')

for i, let in enumerate(letters):
    let.save(f'generated_examples_output/alphabet/{i:04}.jpg')

profiles = []
alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
for i in range(52):
    image = load_image(f'generated_examples_output/alphabet/{i:04}.jpg')
    profile_x, profile_y = get_profiles(image, get_mode(image))
    # print(f'{profile_x} - {profile_y}')
    profiles.append({
        'letter': alphabet[i],
        'profile_x': profile_x,
        'profile_y': profile_y
    })

with open('profiles.json', 'w') as outfile:
    outfile.write(json.dumps(
        profiles,
        indent=4,
        separators=(',', ': ')
    ))
print(profiles[26]['letter'])
plt.plot(range(1, 15), profiles[26]['profile_x'])
plt.show()
plt.plot(range(1, 10), profiles[26]['profile_y'])
plt.show()