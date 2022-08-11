#!/usr/bin/env python3

import datetime
import os
from xml.etree import ElementTree as ET


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
    <style>

    body {
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }

    img {
        width: 150px;
        height: 150px;
    }
    </style>
    ''')

    lines.append('<h1>spanning tree art</h1>')

    for p in svg_paths:
        lines.append(f'<a href="/{p}"><img src="/{p}"></a>')

    lines.append('</html>')

    with open('index.html', 'w') as outfile:
        outfile.write('\n'.join(lines))
