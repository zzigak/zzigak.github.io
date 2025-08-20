from codebank import *

def main():
    c1 = tuple(map(int, input().split()))
    c2 = tuple(map(int, input().split()))
    c3 = tuple(map(int, input().split()))
    # build loci
    if c1[2] == c2[2]:
        locus1 = ('line', perpendicular_bisector(c1, c2))
    else:
        locus1 = ('circle', apollonian_circle(c1, c2))
    if c1[2] == c3[2]:
        locus2 = ('line', perpendicular_bisector(c1, c3))
    else:
        locus2 = ('circle', apollonian_circle(c1, c3))
    # intersect loci
    pts = []
    t1, v1 = locus1
    t2, v2 = locus2
    if t1 == 'line' and t2 == 'line':
        p = intersect_lines(v1, v2)
        if p is not None:
            pts = [p]
    elif t1 == 'line' and t2 == 'circle':
        pts = line_circle_intersection(v1, v2)
    elif t1 == 'circle' and t2 == 'line':
        pts = line_circle_intersection(v2, v1)
    else:
        pts = circle_circle_intersection(v1, v2)
    if not pts:
        return
    if len(pts) == 1:
        x, y = pts[0]
    else:
        x, y = max(((angle_of_observation(c1, p), p) for p in pts))[1]
    print(f"{x:.5f} {y:.5f}")

if __name__ == "__main__":
    main()