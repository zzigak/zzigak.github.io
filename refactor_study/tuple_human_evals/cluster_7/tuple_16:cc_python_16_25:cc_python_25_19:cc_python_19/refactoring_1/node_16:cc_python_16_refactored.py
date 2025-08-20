from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    ans = [-1] * (n + 1)
    for i in range(n, -1, -1):
        if ans[i] == -1:
            z = compute_complement(i)
            ans[i] = z
            ans[z] = i
    m = sum(i ^ ans[i] for i in range(n + 1))
    print(m)
    print(*ans)

if __name__ == "__main__":
    main()