from codebank import *

def main():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    x = pts[-1]
    # nearest neighbor to x
    j = min(range(n-1), key=lambda i: norm_sq(sub(pts[i], x)))
    y = pts[j]
    # nearest point to x not collinear with x,y
    k = min((i for i in range(n-1) if i != j and not collinear(x, y, pts[i])),
            key=lambda i: norm_sq(sub(pts[i], x)))
    print(j+1, k+1, n)

if __name__ == "__main__":
    main()