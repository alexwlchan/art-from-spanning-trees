#!/usr/bin/env python3

import os


def find_svg_paths():
    for name in os.listdir("images"):
        if name.endswith(".svg"):
            yield os.path.join("images", name)


if __name__ == '__main__':
    svg_paths = sorted(
        find_svg_paths(),
        key=lambda p: os.stat(p).st_mtime,
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
