from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    circles = [tuple(map(int, input().split())) for _ in range(3)]
    s1 = locus_between_circles(circles[0], circles[1])
    s2 = locus_between_circles(circles[0], circles[2])
    candidates = intersect_shapes(s1, s2)
    if not candidates:
        return
    x1, y1, r1 = circles[0]
    best_pt = None
    best_ang = -1.0
    for x, y in candidates:
        ang = get_view_angle(x1, y1, r1, x, y)
        if ang >= best_ang:
            best_ang = ang
            best_pt = (x, y)
    print(f"{best_pt[0]:.5f} {best_pt[1]:.5f}")

if __name__ == "__main__":
    main()