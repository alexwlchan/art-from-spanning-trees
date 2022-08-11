#!/usr/bin/env python3

import datetime
import os
from xml.etree import ElementTree as ET


CAPTIONS = {
    "circle_Wed 10 Aug 2022 12:54:14 BST.svg": {
        "date": datetime.date(2022, 8, 10),
        "text": "i tried to make some spider’s web-like graphs, but with straight edges instead of curves. these start to look quite interesting, but i was still working out the kinks &ndash; these graphs aren’t always connected, and sometimes there are loops"
    },
    "circle_Wed 10 Aug 2022 07:11:33 BST.svg": {
        "date": datetime.date(2022, 8, 10),
        "text": "i tried to make a sort of spider's web-like graph, with concentric rings and spokes coming out from the centre. i didn’t really know how to draw arcs properly, so the curves aren’t in the right place &ndash; a lot of these have loops or the lines don’t meet each other properly. i liked the idea, but shelved the curves for a bit"
    },
    "tringle_Wed 10 Aug 2022 06:33:36 BST.svg": {
        "date": datetime.date(2022, 8, 10),
        "text": "i discovered a function called <code><a href=\"https://networkx.org/documentation/stable/reference/generated/networkx.generators.lattice.triangular_lattice_graph.html?highlight=triangular+lattice#networkx.generators.lattice.triangular_lattice_graph\">triangular_lattice_graph</a></code> that dropped straight into my code and made some slightly different pictures. i’m still not really sure what it’s meant to be used for but i think these graphs look nice"
    },
    "Wed 10 Aug 2022 06:23:31 BST.svg": {
        "date": datetime.date(2022, 8, 10),
        "text": "my earliest experiments, drawing graphs on a simple 2D square lattice"
    },
    "Wed 10 Aug 2022 06:17:26 BST.svg": {
        "date": datetime.date(2022, 8, 10),
        "text": "a very early sketch. i must have mucked up the coordinates"
    }
}


def find_svg_paths():
    for name in os.listdir("images"):
        if name.endswith(".svg"):
            path = os.path.join("images", name)

            # filter out invalid SVG
            try:
                root = ET.parse(path).getroot()
            except ET.ParseError as err:
                continue

            yield path


def get_time(p):
    if 'Aug 2022' in p:
        timestamp = p.split()[4]
        hour, minute, second = timestamp.split(':')

        return datetime.datetime(
            2022, 7, 10, int(hour), int(minute), int(second)
        ).timestamp()
    else:
        return os.stat(p).st_mtime


if __name__ == '__main__':
    for p in find_svg_paths():
        print(p, get_time(p))

    svg_paths = sorted(
        find_svg_paths(),
        key=lambda p: get_time(p),
        reverse=True
    )

    lines = ['<html>']

    lines.append('''
    <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <title>spanning tree art</title>
    </head>
    ''')

    lines.append('''
    <style>

    p {
        max-width: 750px;
    }

    body {
        max-width: 950px;
        margin-left: auto;
        margin-right: auto;
        padding: 1em;
        line-height: 1.25em;
    }

    img {
        width: 150px;
        height: 150px;
    }
    </style>
    ''')

    lines.append('<h1>spanning tree art</h1>')

    lines.append('''
    <p>this is some procedurally generated art using <a href="https://en.wikipedia.org/wiki/Minimum_spanning_tree">maximum spanning trees</a>.</p>

    <p>how it works:</p>
    <ol>
    <li>create a <a href="https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)">graph</a> &ndash; in the mathematical sense, a network of nodes and edges</li>
    <li>assign random weights to each edge</li>
    <li>find a maximally spanning tree of the weighted graph. visit every point, use as many edges as possible, but never have a loop</li>
    </ol>
    <p>this is a gallery of some of the pictures i&rsquo;ve made this way. i think they&rsquo;re pretty.</p>

    <p>made with &lt;3 by <a href="https://alexwlchan.net">alexwlchan</a>. code on <a href="https://github.com/alexwlchan/art-from-spanning-trees">github</a></p>

    <hr/>
    ''')

    for p in svg_paths:
        if os.path.basename(p) in CAPTIONS:
            caption = CAPTIONS[os.path.basename(p)]
            lines.append(f"<p><strong>{caption['date'].strftime('%d %B %Y').lower()} / </strong> {caption['text']}</p>")
        lines.append(f'<a href="/{p}"><img src="/{p}"></a>')

    lines.append('</html>')

    with open('index.html', 'w') as outfile:
        outfile.write('\n'.join(lines))
