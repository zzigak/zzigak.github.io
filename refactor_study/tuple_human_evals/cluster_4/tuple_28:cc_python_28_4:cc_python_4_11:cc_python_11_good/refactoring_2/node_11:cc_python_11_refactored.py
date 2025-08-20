from codebank import *

def main():
    c1 = tuple(map(int, input().split()))
    c2 = tuple(map(int, input().split()))
    c3 = tuple(map(int, input().split()))
    locus12 = locus_equal_angle(c1, c2)
    locus13 = locus_equal_angle(c1, c3)
    pts = intersect_loci(locus12, locus13)
    best = None
    best_ang = -1
    for x, y in pts:
        ang = get_viewing_angle(c1[0], c1[1], c1[2], x, y)
        if ang > best_ang:
            best_ang = ang
            best = (x, y)
    if best:
        print(f"{best[0]:.5f} {best[1]:.5f}")

if __name__ == "__main__":
    main()