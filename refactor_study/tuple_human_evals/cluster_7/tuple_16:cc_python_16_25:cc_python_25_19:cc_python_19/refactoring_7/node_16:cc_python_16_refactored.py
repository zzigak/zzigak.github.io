from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    ans = [0] * (n + 1)
    used = [False] * (n + 1)
    for i in range(n, -1, -1):
        if not used[i]:
            j = bit_flipped(i)
            used[i] = used[j] = True
            ans[i] = j
            ans[j] = i
    total = sum(i ^ ans[i] for i in range(n + 1))
    print(total)
    print(*ans)

if __name__ == "__main__":
    main()