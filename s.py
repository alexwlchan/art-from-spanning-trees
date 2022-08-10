import random
import networkx as nx

G = nx.Graph()

max_width = 10

for x in range(1, max_width):
    for y in range(1, max_width):
        if x + 1 <= max_width:
            G.add_edge(f"{x},{y}", f"{x+1},{y}", weight=-1 * abs(random.random()))
        if y + 1 <= max_width:
            G.add_edge(f"{x},{y}", f"{x},{y+1}", weight=-1 * abs(random.random()))

T = nx.tree.minimum_spanning_tree(G)

print(f'<svg viewBox="0 0 {max_width + 1}0 {max_width + 1}0" xmlns="http://www.w3.org/2000/svg">')

for start, end in T.edges:
    x2, y2 = start.split(',')
    x1, y1 = end.split(',')
    print(f'<line x2="{x2}0" y2="{y2}0" x1="{x1}0" y1="{y1}0" stroke="#aaa" stroke-width="1" stroke-linecap="round"/>')

print('</svg>')

# print(T.edges)

# nx.draw(T, pos, edge_color='r', width=3.0)