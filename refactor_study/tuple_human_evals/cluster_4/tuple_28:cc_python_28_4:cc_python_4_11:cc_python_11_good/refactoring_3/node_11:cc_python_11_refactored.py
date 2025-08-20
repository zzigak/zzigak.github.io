from codebank import *

def main():
    c1 = tuple(map(int, input().split()))
    c2 = tuple(map(int, input().split()))
    c3 = tuple(map(int, input().split()))
    l1 = get_locus(c1, c2)
    l2 = get_locus(c1, c3)
    pts = intersect_locus(l1, l2)
    best = None; best_ang = -1.0
    for p in pts:
        ang = get_angle(c1, p)
        if ang is not None and ang > best_ang:
            best_ang = ang; best = p
    if best:
        print(f"{best[0]:.5f} {best[1]:.5f}")

if __name__ == "__main__":
    main()