import matplotlib.pyplot as plt
import numpy as np

config = {
    "seed": np.random.randint(100000),
    # "seed": 34358,
    "act_centers": 7,
    "num_centers": 7, # Don't exceed 8 cuz I only put in 8 colors
    "iters": 100,
    "jitters": 1,
    "save_file": None # Put file name if you wish to save as video
}

print(f"Using config {config}")

#========================
# Satisfying seeds: 4619, 73312, 58126, 39231 | I forgot how many centers these seeds had
#-----------------------
# seed = 
seed = config['seed']

np.random.seed(seed)


width  = 100
height = 100
buffer = 10
clusize = 20
plt.xlim((0-buffer,width+buffer))
plt.ylim((0-buffer,height+buffer))

act_centers = config['act_centers']
num_centers = config['num_centers']
centers = np.random.rand(act_centers, 2) * (width, height)
# print("True Centers")
# print(centers)
plt.scatter(*centers.T, c='gray')

#lets do 100 points for each centers

points = []

for center in centers:
    points.append((np.random.rand(100, 2)-0.5)*clusize+center)
points = np.concatenate(points)
ptcol = plt.scatter(*points.T, c=[(0,0,0,0.2)], s=1)


clucenters = (np.random.rand(num_centers, 2)-0.5) * np.std(points, 0) + np.mean(points, 0)
# print("Random centers")
# print(clucenters)

colors = ['r','b','tab:green', 'tab:orange', 'tab:purple', 'c', 'y', 'tab:brown'][:num_centers]
ctcol = plt.scatter(*clucenters.T, marker='x', color=colors)

def init():
    global clucenters
    # np.random.seed(seed)
    clucenters = (np.random.rand(num_centers, 2)-0.5) * np.std(points, 0) + np.mean(points, 0)
    ctcol.set_offsets(clucenters)

def get_color_points():
    return [
        colors[min(range(num_centers), key=lambda i: np.linalg.norm(p - clucenters[i]))]
        for p in points
    ]
# get_color_points()
ptcol.set_color(get_color_points())

def color_to_idx(c):
    for i, oc in enumerate(colors):
        if c==oc:
            return i
    raise Exception(f"Color {c} is not valid in {colors}")
def get_new_centers():
    cols = get_color_points()
    groups = [[cen] for cen in clucenters]
    for p, c in zip(points, cols):
        groups[color_to_idx(c)].append(p)
    
    for g in groups:
        g.extend(
            (np.random.rand(config['jitters'], 2)-0.5) * np.std(points, 0) + np.mean(points, 0)
        )
    
    
    centers = []
    for g in groups:
        centers.append(sum(g, np.array([0,0]))/len(g))
    return np.array(centers)

# print("New Centers")
# print(get_new_centers())

new_centers = plt.scatter(*get_new_centers().T, marker='1', c=colors)
new_centers.set_color(None)
ptcol.set_color('tab:gray')

states = {
    0: "Centroids Placed",
    1: "Clusters Made",
    2: "New Centroids Calculated"
}

cur_step = 0
def update(frame_no):
    plt.title(frame_no)
    global cur_step
    if cur_step == 0:
        ptcol.set_color(get_color_points())
        cur_step = 1
    elif cur_step == 1:
        new_centers.set_offsets(get_new_centers())
        new_centers.set_color(colors)
        cur_step = 2
    elif cur_step == 2:
        new_centers.set_color(None)
        global clucenters
        clucenters = get_new_centers()
        ctcol.set_offsets(clucenters)
        cur_step = 0

import matplotlib.animation as anim

anime = anim.FuncAnimation(plt.gcf(), update, config['iters'], init_func=init)
if config['save_file']:
    anime.save(config['save_file'])
    





plt.get_current_fig_manager().full_screen_toggle()
plt.show()