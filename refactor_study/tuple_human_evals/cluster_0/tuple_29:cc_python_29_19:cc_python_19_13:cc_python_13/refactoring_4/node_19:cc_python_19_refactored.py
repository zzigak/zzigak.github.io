from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    child = [[] for _ in range(n)]
    for i in range(2, n + 1):
        p = int(input()) - 1
        child[p].append(i - 1)
    print("Yes" if is_spruce(child) else "No")

if __name__ == "__main__":
    main()