import sys
from codebank import *

def main():
    input = sys.stdin.readline
    n = int(input())
    children = [[] for _ in range(n)]
    for i in range(1, n):
        p = int(input()) - 1
        children[p].append(i)
    print("Yes" if is_spruce(children) else "No")

if __name__ == "__main__":
    main()