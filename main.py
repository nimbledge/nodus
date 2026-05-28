import matplotlib.pyplot as plt
import numpy as np
import random
from time import sleep
import networkx as nx
import matplotlib.animation as animation


universe = nx.Graph()
for i in range(50):
    universe.add_node(
        i,
        pos=np.array([random.gauss(0, 5), random.gauss(0, 5), random.gauss(0, 1)]),
        vel=np.array([0,0,0]),
        stability=1,
        owner=None,
    )


def update_edges():
    for u, v in universe.edges:
        universe.edges[u, v]['distance'] = np.linalg.norm(
            universe.nodes[u]['pos'] - universe.nodes[v]['pos']
        )


def draw_graph(ax):
    ax.clear()
    xs = [universe.nodes[n]['pos'][0] for n in universe.nodes]
    ys = [universe.nodes[n]['pos'][1] for n in universe.nodes]
    zs = [universe.nodes[n]['pos'][2] for n in universe.nodes]

    ax.scatter(xs, ys, zs, c='blue', s=50)
    for u, v in universe.edges:
        x_line = [universe.nodes[u]['pos'][0], universe.nodes[v]['pos'][0]]
        y_line = [universe.nodes[u]['pos'][1], universe.nodes[v]['pos'][1]]
        z_line = [universe.nodes[u]['pos'][2], universe.nodes[v]['pos'][2]]
        ax.plot(x_line, y_line, z_line, c='gray', alpha=0.5)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Universe Nodes and Connections')
    ax.set_xlim(-15, 15)
    ax.set_ylim(-15, 15)
    ax.set_zlim(-3, 3)


# TODO: generate edges
update_edges()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def animate(frame):
    tick()
    draw_graph(ax)

def tick():
    center = np.array([0.0, 0.0, 0.0])
    for node in universe.nodes:
        pos = universe.nodes[node]['pos']
        r = pos - center
        weight = np.exp(-np.linalg.norm(r)**2 / 50.0)
        curl = np.array([-r[1], r[0], 0]) * 0.05 * weight
        universe.nodes[node]['pos'] += curl
        universe.nodes[node]['stability'] -= random.uniform(0.01, 0.1)
        if universe.nodes[node]['stability'] <= 0.3:
            universe.nodes[node]['pos'] += np.random.uniform(-0.1, 0.1, 3)
            universe.nodes[node]['stability'] = 1
    update_edges()

anim = animation.FuncAnimation(fig, animate, frames=300, interval=1)
anim.save('universe.gif', writer='pillow')

# while True:
#     tick()
#     draw_graph(ax)
#     plt.savefig('universe.png')
#     sleep(1)
