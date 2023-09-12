import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
np.random.seed(10)
def generate_increasing_random_numbers(n):
    if n <= 0:
        return []

    numbers = [random.uniform(0, 2*np.pi) for i in range(n)]
    numbers.sort()

    return numbers

def polygon_generator(n):
    random_numbers = generate_increasing_random_numbers(n)
    vertices =[]
    for i in range(n):
        if random_numbers[i] > np.pi/2 and random_numbers[i] < 3*np.pi/2:
            x = -5*np.random.random(1)[0]
            y = x*np.tan(random_numbers[i])
        else:
            x = 5*np.random.random(1)[0]
            y = x*np.tan(random_numbers[i])

        vertices.append((x,y))
    # print(vertices)
    # y_coordinates = [y[1] for y in vertices]
    # vertices.append(vertices[0])
    # path = mpath.Path(vertices)
    # patch = mpatches.PathPatch(path, lw=2,facecolor='white', alpha = 0.5)
    # fig, ax = plt.subplots()
    # ax.add_patch(patch)
    # ax.set_xlim(-5,5)
    # ax.set_ylim(min(y_coordinates)-0.5,max(y_coordinates)+0.5)

    # plt.show() 
 
    return vertices
        
polygons = []

for i in range(4,200):
    polygons.append(polygon_generator(i))