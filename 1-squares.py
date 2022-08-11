#!/usr/bin/env python3

import random

import networkx as nx

from core import generate_spanning_tree_graph, render_svg


def generate_square_graph(*, rows, columns):
    G = nx.grid_2d_graph(rows + 1, columns + 1)

    # The networkx generated square lattice starts at (0, 0).
    #
    # This is moderately annoying for rendering in SVG, so adjust the
    # graph so it starts at (1, 1).
    adjusted_G = nx.Graph()

    for (start_x, start_y), (end_x, end_y) in G.edges:
        adjusted_G.add_edge((start_x + 1, start_y + 1), (end_x + 1, end_y + 1))

    return adjusted_G


def get_svg_path_commands(square_G):
    for ((x1, y1), (x2, y2)) in square_G.edges:
        yield f'M {x1},{y1} L {x2},{y2}'


def get_bounds(G):
    min_width = min(x for (x, _) in G.nodes)
    min_height = min(y for (_, y) in G.nodes)

    max_width = max(x for (x, _) in G.nodes)
    max_height = max(y for (_, y) in G.nodes)

    return {
        'width': (min_width, max_width),
        'height': (min_width, max_width)
    }




if __name__ == '__main__':
    G = generate_square_graph(rows=3, columns=3)
    T = generate_spanning_tree_graph(G)

    bounds = get_bounds(G)
    path_commands = get_svg_path_commands(T)

    styles = {
        'background_color': '#ffece0',
        'stroke_color': '#a33f00',
        'stroke_width': abs(random.uniform(0.01, 0.7))
    }

    print(render_svg(path_commands, bounds, styles))
