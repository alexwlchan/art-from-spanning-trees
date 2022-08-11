import random

import networkx as nx


def generate_spanning_tree_graph(G, *, rand=None):
    if rand is None:
        rand = random.Random()

    # Create a copy of the graph with randomly weighted edges, then
    # identify a maximal spanning tree
    weighted_G = nx.Graph()

    for (start, end) in G.edges:
        weight = -1 * abs(rand.random())
        weighted_G.add_edge(start, end, weight=weight)

    return nx.tree.minimum_spanning_tree(weighted_G)


def render_svg(path_commands, bounds, styles=None):
    if styles is None:
        styles = {}

    # We add a border of 1 unit around the bounding box, so all the
    # lines should be inside the graph
    width = bounds["width"][1] - bounds["width"][0] + 2
    height = bounds["height"][1] - bounds["height"][0] + 2

    if "background_color" in styles:
        style = f' style="background-color: {styles["background_color"]};"'
    else:
        style = ""

    lines = [
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg"{style}>'
    ]

    # Add some styles so we can see what we're drawing.
    lines.append(
        f"""
    <defs>
      <style>
        path {{
          stroke: {styles.get("stroke_color", "#aaa")};
          stroke-width: {styles.get("stroke_width", 0.1)};
          stroke-linecap: round;
          fill: none;
        }}
      </style>
    </defs>
    """
    )

    # Translate all the paths so they're not right on the edge of
    # the image.
    x_adjustment = 1 - bounds["width"][0]
    y_adjustment = 1 - bounds["height"][0]
    lines.append(f'<svg x="{x_adjustment}" y="{y_adjustment}">')

    for command in path_commands:
        lines.append(f'<path d="{command}"/>')

    # Close the adjustment SVG
    lines.append("</svg>")

    # Close the overall SVG
    lines.append("</svg>")

    return "\n".join(lines)


def get_svg_line_path_commands(square_G):
    for ((x1, y1), (x2, y2)) in square_G.edges:
        yield f"M {x1},{y1} L {x2},{y2}"


def get_xy_bounds(G):
    min_width = min(x for (x, _) in G.nodes)
    min_height = min(y for (_, y) in G.nodes)

    max_width = max(x for (x, _) in G.nodes)
    max_height = max(y for (_, y) in G.nodes)

    return {"width": (min_width, max_width), "height": (min_height, max_height)}


def delete_some_nodes(G):
    nodes = random.sample(list(G.nodes), random.randint(1, len(G.nodes) // 5))
    for n in nodes:
        G.remove_node(n)
