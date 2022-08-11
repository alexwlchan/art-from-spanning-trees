#!/usr/bin/env python3

import random

import networkx as nx

from core import generate_spanning_tree_graph, get_svg_line_path_commands, get_xy_bounds, render_svg


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


if __name__ == '__main__':
    G = generate_square_graph(rows=3, columns=3)
    T = generate_spanning_tree_graph(G)

    bounds = get_xy_bounds(G)
    path_commands = get_svg_line_path_commands(T)

    styles = {
        'background_color': '#ffece0',
        'stroke_color': '#a33f00',
        'stroke_width': abs(random.uniform(0.01, 0.7))
    }

    print(render_svg(path_commands, bounds, styles))
