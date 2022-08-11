#!/usr/bin/env python3

import math
import random
import re

import networkx as nx

from core import generate_spanning_tree_graph, get_svg_line_path_commands, get_xy_bounds, render_svg


def generate_radial_graph(*, ring_count, spoke_count, include_centre):
    G = nx.Graph()

    # The graph is made up of concentric rings.
    #
    # The rings are labelled R1, R1, …, Rn.  The innermost ring is R0,
    # and the ring number increases as you go outwards.
    #
    # Along each ring are points intersecting the spokes.  These are numbered
    # S0, S1, …, Sk for each point.  S0 is the upwards vertical spoke, and
    # then they go clockwise around the ring.
    #
    # Individual nodes in the graph are labelled Ri-Sj for the jth spoke
    # on the ith ring.
    #
    # There's also an optional centre node.
    for ring_number in range(1, ring_count + 1):
        for spoke_number in range(spoke_count):

            this_point = f"R{ring_number}-S{spoke_number}"

            # Connect to the next spoke, clockwise.
            if spoke_number + 1 == spoke_count:
                G.add_edge(this_point, f"R{ring_number}-S0")
            else:
                G.add_edge(this_point, f"R{ring_number}-S{spoke_number+1}")

            # If we're in the innermost ring and we have a centre node,
            # we need to connect to that.
            if ring_number == 1 and include_centre:
                G.add_edge(this_point, "C")

            # If we're in another ring, we need to join to the corresponding
            # point on the next innermost ring.
            if ring_number > 1:
                G.add_edge(this_point, f"R{ring_number - 1}-S{spoke_number}")

    return G


def get_radial_bounds(ring_count):
    return {
        'width': (1, 1 + ring_count * 2),
        'height': (1, 1 + ring_count * 2)
    }


def parse_node(node_label):
    if node_label == "C":
        return "C"
    else:
        m = re.match(r'^R(?P<ring_number>\d+)-S(?P<spoke_number>\d+)$', node_label)
        return {
            'ring_number': int(m.group('ring_number')),
            'spoke_number': int(m.group('spoke_number'))
        }


def xy_coords(*, ring_number, spoke_number, ring_count, spoke_count):
    centre_x = ring_count + 1
    centre_y = ring_count + 1

    return [
        centre_x + ring_number * math.sin(math.pi - spoke_number / spoke_count * 2 * math.pi),
        centre_y + ring_number * math.cos(math.pi - spoke_number / spoke_count * 2 * math.pi)
    ]


def get_circular_arc_path_command(*, centre_x, centre_y, radius, start_angle, sweep_angle, angle_unit, sweep_flag=1):
    """
    Returns a path command to draw a circular arc in an SVG <path> element.

    See https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths#line_commands

    From https://alexwlchan.net/files/2022/create_circular_arc_paths.py
    """
    if angle_unit == "radians":
        pass
    elif angle_unit == "degrees":
        start_angle = start_angle / 180 * math.pi
        sweep_angle = sweep_angle / 180 * math.pi
    else:
        raise ValueError(f"Unrecognised angle unit: {angle_unit}")

    # Work out the start/end points of the arc using trig identities
    start_x = centre_x + radius * math.sin(start_angle)
    start_y = centre_y - radius * math.cos(start_angle)

    end_x = centre_x + radius * math.sin(start_angle + sweep_angle)
    end_y = centre_y - radius * math.cos(start_angle + sweep_angle)

    # An arc path in SVG defines an ellipse/curve between two points.
    # The `x_axis_rotation` parameter defines how an ellipse is rotated,
    # if at all, but circles don't change under rotation, so it's irrelevant.
    x_axis_rotation = 0

    # For a given radius, there are two circles that intersect the
    # start/end points.
    #
    # The `sweep-flag` parameter determines whether we move in
    # a positive angle (=clockwise) or negative (=counter-clockwise).
    # I'only doing clockwise sweeps, so this is constant.
    # sweep_flag = sweep_flag

    # There are now two arcs available: one that's more than 180 degrees,
    # one that's less than 180 degrees (one from each of the two circles).
    # The `large-arc-flag` decides which to pick.
    if sweep_angle > math.pi:
        large_arc_flag = 1
    else:
        large_arc_flag = 0

    return (
        f"M {start_x} {start_y} "
        f"A {radius} {radius} "
        f"{x_axis_rotation} {large_arc_flag} {sweep_flag} {end_x} {end_y}"
    )

def get_svg_radial_path_commands(radial_G, *, ring_count, spoke_count, arc_type):
    if arc_type not in ("straight", "curved", 'inner_curve', 'alternating_curves'):
        raise ValueError(f"Unrecognised arc type: {arc_type!r}")

    centre_x = ring_count + 1
    centre_y = ring_count + 1

    for (start, end) in radial_G.edges:
        import sys; print(start, end, file=sys.stderr)
        # if 'C' != start and 'C' != end:
        #     continue
        #
        # if 'S1' not in start and 'S1' not in end:
        #     continue

        start = parse_node(start)
        end = parse_node(end)

        # If either node is the centre, we draw a straight spoke to
        # the point on the innermost ring.
        if start == 'C':
            end_x, end_y = xy_coords(**end, ring_count=ring_count, spoke_count=spoke_count)
            yield f'M {centre_x},{centre_y} L {end_x},{end_y}'
        elif end == 'C':
            start_x, start_y = xy_coords(**start, ring_count=ring_count, spoke_count=spoke_count)
            yield f'M {centre_x},{centre_y} L {start_x},{start_y}'

        # If both nodes are on the same spoke but different rings,
        # we draw a straight spoke between the two rings
        elif start['spoke_number'] == end['spoke_number']:
            start_x, start_y = xy_coords(**start, ring_count=ring_count, spoke_count=spoke_count)
            end_x, end_y = xy_coords(**end, ring_count=ring_count, spoke_count=spoke_count)

            yield f'M {start_x} {start_y} L {end_x} {end_y}'

        # If both nodes are on the same ring but different spokes, we
        # draw an arc between them.
        else:
            # if start_x
#
            start_x, start_y = xy_coords(**start, ring_count=ring_count, spoke_count=spoke_count)
            end_x, end_y = xy_coords(**end, ring_count=ring_count, spoke_count=spoke_count)

            both_spoke_numbers = [start['spoke_number'], end['spoke_number']]
            if 0 in both_spoke_numbers and 1 not in both_spoke_numbers:
                spoke_number = max(both_spoke_numbers)
            else:
                spoke_number = min(both_spoke_numbers)

            # import sys; print(start, end, file=sys.stderr)
            if arc_type == "straight":
                yield f'M {start_x} {start_y} L {end_x} {end_y}'
            else:
                yield get_circular_arc_path_command(
                    centre_x=centre_x,
                    centre_y=centre_y,
                    radius=start['ring_number'],
                    start_angle=spoke_number / spoke_count * 2 * math.pi,
                    sweep_angle=2 * math.pi / spoke_count,
                    angle_unit='radians',
                    sweep_flag=spoke_number % 2 if arc_type == 'alternating_curves' else 0 if arc_type == 'curved' else 1
                )

        # import sys; print(start, end, file=sys.stderr)
        # start, end = edge.split("-")
    # return []


if __name__ == '__main__':
    ring_count = random.randint(3, 15)
    spoke_count = random.randint(2, 20)

    G = generate_radial_graph(ring_count=ring_count, spoke_count=spoke_count, include_centre=random.choice([True, False]))
    T = generate_spanning_tree_graph(G)

    bounds = get_radial_bounds(ring_count)
    path_commands = get_svg_radial_path_commands(T, ring_count=ring_count, spoke_count=spoke_count, arc_type=random.choice(['curved', 'alternating_curves', 'inner_curve', 'straight']))

    styles = {
        'background_color': '#222',
        'stroke_color': '#006aff',
        'stroke_width': abs(random.uniform(0.01, 0.5))
    }

    print(render_svg(path_commands, bounds, styles))
