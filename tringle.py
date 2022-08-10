import random
import networkx as nx

G = nx.triangular_lattice_graph(10, 10)

for i,j in G.edges():
    G[i][j]['weight'] = -1 * abs(random.random())

# for edge in G.edges:
#     print(edge)

max_width = 10
#
# for x in range(1, max_width):
#     for y in range(1, max_width):
#         if x + 1 <= max_width:
#             G.add_edge(f"{x},{y}", f"{x+1},{y}", weight=-1 * abs(random.random()))
#         if y + 1 <= max_width:
#             G.add_edge(f"{x},{y}", f"{x},{y+1}", weight=-1 * abs(random.random()))

# https://caam37830.github.io/book/05_graphs/networkx.html#spanning-trees
T = nx.tree.minimum_spanning_tree(G)

print(f'<svg viewBox="0 0 70 120" xmlns="http://www.w3.org/2000/svg">')

import sys

# for n in T.edges:
#     print(n, file=sys.stderr)

for ((x1, y1), (x2, y2)) in T.edges:
    print(f'<line x2="{x2+1}0" y2="{y2+1}0" x1="{x1+1}0" y1="{y1+1}0" stroke="#aaa" stroke-width="1" stroke-linecap="round"/>')

print('</svg>')

# print(T.edges)

# nx.draw(T, pos, edge_color='r', width=3.0)