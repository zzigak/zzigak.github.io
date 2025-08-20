from codebank import *

def main():
    n = int(input())
    pts = [tuple(map(int, input().split())) + (i+1,) for i in range(n)]
    x = pts[-1]
    others = pts[:-1]
    y = min(others, key=lambda t: norm_sq(sub(x, t)))
    z_candidates = [t for t in others if t != y and not collinear(x, y, t)]
    z = min(z_candidates, key=lambda t: norm_sq(sub(x, t)))
    print(x[2], y[2], z[2])

if __name__ == "__main__":
    main()