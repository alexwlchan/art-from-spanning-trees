import math

# const cos = Math.cos;
# const sin = Math.sin;
# const π = Math.PI;

def f_rotate_matrix(x):
    return [
        [math.cos(x), -math.sin(x)],
        [math.sin(x), math.cos(x)]
    ]

def f_vec_add(v1, v2):
    a1, a2 = v1
    b1, b2 = v2
    return [a1 + b1, a2 + b2]

def f_matrix_times(arg1, arg2):
    (a, b), (c, d) = arg1
    (x, y) = arg2
    return [ a * x + b * y, c * x + d * y]

# const f_matrix_times = (( [[a,b], [c,d]], [x,y]) => [ a * x + b * y, c * x + d * y]);
# const f_rotate_matrix = (x => [[cos(x),-sin(x)], [sin(x), cos(x)]]);
# const f_vec_add = (([a1, a2], [b1, b2]) => [a1 + b1, a2 + b2]);
#
# const f_svg_ellipse_arc = (([cx,cy],[rx,ry], [t1, Δ], φ ) => {
# /* [
# returns a SVG path element that represent a ellipse.
# cx,cy → center of ellipse
# rx,ry → major minor radius
# t1 → start angle, in radian.
# Δ → angle to sweep, in radian. positive.
# φ → rotation on the whole, in radian
# URL: SVG Circle Arc http://xahlee.info/js/svg_circle_arc.html
# Version 2019-06-19
#  ] */

def generate_svg_path(cx, cy, rx, ry, t1, delta, phi):
    delta = delta % (2 * math.pi)
    rotMatrix = f_rotate_matrix(phi)
    sX, sY = f_vec_add(
        f_matrix_times(
            rotMatrix,
            [rx * math.cos(-t1), ry * math.sin(-t1)]
        ),
        [cx, cy]
    )
    eX, eY = f_vec_add(
        f_matrix_times(
            rotMatrix,
            [rx * math.cos(-t1 + delta), ry * math.sin(-t1 + delta)]
        ),
        [cx, cy]
    )
    fA = 1 if delta > math.pi else 0
    fS = 1 if delta > 0 else 0

    return f'<path d="M {sX} {sY} A {rx} {ry} {phi / 2 * math.pi * 360} {fA} {fS} {eX} {eY}" stroke="#aaa" stroke-width="1" stroke-linecap="round" fill="none"/>'

# Δ = Δ % (2* math.pi);
# const rotMatrix = f_rotate_matrix (φ);
# const [sX, sY] = ( f_vec_add ( f_matrix_times ( rotMatrix, [rx * cos(t1), ry * sin(t1)] ), [cx,cy] ) );
# const [eX, eY] = ( f_vec_add ( f_matrix_times ( rotMatrix, [rx * cos(t1+Δ), ry * sin(t1+Δ)] ), [cx,cy] ) );
# const fA = ( (  Δ > π ) ? 1 : 0 );
# const fS = ( (  Δ > 0 ) ? 1 : 0 );
# const path_2wk2r = document.createElementNS("http://www.w3.org/2000/svg", "path");
# path_2wk2r.setAttribute("d", "M " + sX + " " + sY + " A " + [ rx , ry , φ / (2*π) *360, fA, fS, eX, eY ].join(" "));
# return path_2wk2r;