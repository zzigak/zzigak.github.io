from codebank import *

def main():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    x_idx = n - 1
    x = pts[x_idx]
    y_idx = min(range(n - 1), key=lambda i: norm_sq(sub(x, pts[i])))
    y = pts[y_idx]
    k_idx = min(
        (i for i in range(n)
         if i not in (x_idx, y_idx)
         and not collinear(x, y, pts[i])),
        key=lambda i: norm_sq(sub(x, pts[i]))
    )
    # output 1-based indices
    print(x_idx + 1, y_idx + 1, k_idx + 1)

if __name__ == "__main__":
    main()