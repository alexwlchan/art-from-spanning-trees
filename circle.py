#!/usr/bin/env python3

import networkx as nx, random, math

rings = 4
points = random.randint(5, 30)

cx = 100
cy = 100

G = nx.Graph()

# r = random.Random(0)
r = random.Random()

from svg_arc import generate_svg_path

for ring_number in range(rings):
    for point_number in range(points):
        # It connects to the next point in the circle
        G.add_edge(
            f"R{ring_number}-P{point_number}",
            f"R{ring_number}-P{(point_number + 1) % points}"
        )

        # It connects to the next inner point
        if ring_number < rings - 1:
            G.add_edge(
                f"R{ring_number}-P{point_number}",
                f"R{ring_number + 1}-P{point_number}",
            )
        # or the centre
        else:
            G.add_edge(f"R{ring_number}-P{point_number}", "C")

import sys
# print(G.edges, file=sys.stderr)

for i,j in G.edges():
    G[i][j]['weight'] = -1 * abs(r.random())

# https://caam37830.github.io/book/05_graphs/networkx.html#spanning-trees
T = nx.tree.minimum_spanning_tree(G)

print(f'<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">')

def radius(ring_number):
    return (rings + 1 - ring_number) * 10

def xy_coords(ring_number, point_number):
    return [
        cx + radius(ring_number) * math.sin(math.pi + point_number / points * 2 * math.pi),
        cy + radius(ring_number) * math.cos(math.pi + point_number / points * 2 * math.pi)
    ]

print(T.edges, file=sys.stderr)

for start, end in T.edges:
    if start != 'C' and end != 'C':
        r0, p0 = [int(c[1:]) for c in start.split('-')]
        r1, p1 = [int(c[1:]) for c in end.split('-')]

        if r0 == r1:
            # print(f'r0 = {r0}, p0 = {p0}, r1 = {r1}, p1 = {p1}', file=sys.stderr)
            # print(radius(r0), file=sys.stderr)
            # print(f'<!-- R{r0}-P{p0}, R{r1}-P{p1} -->')

            x1, y1 = xy_coords(r0, p0)
            x2, y2 = xy_coords(r1, p1)

            print(f'<line x2="{x2}" y2="{y2}" x1="{x1}" y1="{y1}" stroke="#aaa" stroke-width="1" stroke-linecap="round"/>')

            # if p1 == points - 1 and p0 == 0:
            #     path = generate_svg_path(
            #         cx = cx,
            #         cy = cy,
            #         rx = radius(r0),
            #         ry = radius(r0),
            #         t1 = p1 / points * 2 * math.pi,
            #         delta = 2 * math.pi / points,
            #         phi = - math.pi / 2
            #     )
            # else:
            #     path = generate_svg_path(
            #         cx = cx,
            #         cy = cy,
            #         rx = radius(r0),
            #         ry = radius(r0),
            #         t1 = p0 / points * 2 * math.pi,
            #         delta = 2 * math.pi / points,
            #         phi = - math.pi / 2
            #     )
            # print(path)
        else:
            x1, y1 = xy_coords(r0, p0)
            x2, y2 = xy_coords(r1, p1)

            print(f'<line x2="{x2}" y2="{y2}" x1="{x1}" y1="{y1}" stroke="#aaa" stroke-width="1" stroke-linecap="round"/>')
    elif start == 'C':
        r0, p0 = [int(c[1:]) for c in end.split('-')]

        x1, y1 = xy_coords(r0, p0)
        x2, y2 = cx, cy
        # print(f'<!-- R{r0}-P{p0}, C -->')
        print(f'<line x2="{x2}" y2="{y2}" x1="{x1}" y1="{y1}" stroke="#aaa" stroke-width="1" stroke-linecap="round"/>')
    else:
        r0, p0 = [int(c[1:]) for c in start.split('-')]

        x1, y1 = xy_coords(r0, p0)
        x2, y2 = cx, cy
        # print(f'<!-- R{r0}-P{p0}, C -->')
        print(f'<line x2="{x2}" y2="{y2}" x1="{x1}" y1="{y1}" stroke="#aaa" stroke-width="1" stroke-linecap="round"/>')

    # print(start, end)

print('</svg>')
# print(T.edges)