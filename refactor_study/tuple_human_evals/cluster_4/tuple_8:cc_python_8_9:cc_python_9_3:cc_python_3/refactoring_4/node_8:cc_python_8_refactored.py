from codebank import *

def main():
    n = int(input())
    pts = [tuple(map(int, input().split())) + (i+1,)
           for i in range(n)]
    p0 = pts.pop()
    idx1, p1 = min(enumerate(pts),
                   key=lambda t: dist_sq(p0[:2], t[1][:2]))
    p1 = pts.pop(idx1)
    idx2, p2 = min(
        ((i, pt) for i, pt in enumerate(pts)
         if not collinear(p0[:2], p1[:2], pt[:2])),
        key=lambda t: dist_sq(p0[:2], t[1][:2])
    )
    p2 = pts[idx2]
    print(p0[2], p1[2], p2[2])

if __name__ == "__main__":
    main()