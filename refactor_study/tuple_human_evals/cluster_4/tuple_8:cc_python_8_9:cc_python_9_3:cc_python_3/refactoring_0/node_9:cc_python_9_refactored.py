from codebank import sub, dot

def is_bad(pts, a):
    n = len(pts)
    for b in range(n):
        if b == a: continue
        for c in range(b + 1, n):
            if c == a: continue
            if dot(sub(pts[b], pts[a]), sub(pts[c], pts[a])) > 0:
                return True
    return False

def main():
    n = int(input())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    if n > 11:
        print(0)
        return
    good = [i + 1 for i in range(n) if not is_bad(pts, i)]
    print(len(good))
    for idx in good:
        print(idx)

if __name__ == "__main__":
    main()