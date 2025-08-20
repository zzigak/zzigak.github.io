from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it))
    arr = [int(next(it)) for _ in range(n)]
    p = int(next(it))
    dp_counts = count_subsets_by_size(arr, p)
    ans = 0.0
    denom = 1.0
    for k in range(1, n+1):
        denom *= n - k + 1
        ans += dp_counts[k] / denom
    print(ans)

if __name__ == "__main__":
    main()