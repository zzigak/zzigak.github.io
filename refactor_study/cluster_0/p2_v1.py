# ########## PROGRAM: node_19:cc_python_19 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    parents = [int(input()) for _ in range(n-1)]
    children = build_tree_children(n, parents)
    for v in range(1, n+1):
        if children[v]:
            leaves = sum(1 for u in children[v] if not children[u])
            if leaves < 3:
                print("No")
                return
    print("Yes")

if __name__ == "__main__":
    main()