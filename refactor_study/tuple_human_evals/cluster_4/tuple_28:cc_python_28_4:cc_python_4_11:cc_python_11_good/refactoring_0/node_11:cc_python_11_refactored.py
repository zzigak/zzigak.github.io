from codebank import *

def main():
    x1, y1, r1 = map(int, input().split())
    x2, y2, r2 = map(int, input().split())
    x3, y3, r3 = map(int, input().split())
    p1, p2, p3 = (x1, y1), (x2, y2), (x3, y3)

    s1 = bisector(p1, p2) if r1 == r2 else apollonian_circle(p1, p2, r1, r2)
    s2 = bisector(p1, p3) if r1 == r3 else apollonian_circle(p1, p3, r1, r3)
    candidates = intersect(s1, s2)
    if not candidates:
        return

    best = None
    best_ang = -1
    for pt in candidates:
        ang = observation_angle(x1, y1, r1, pt)
        if ang > best_ang:
            best_ang = ang
            best = pt

    if best is not None:
        print(f"{best[0]:.5f} {best[1]:.5f}")

if __name__ == "__main__":
    main()