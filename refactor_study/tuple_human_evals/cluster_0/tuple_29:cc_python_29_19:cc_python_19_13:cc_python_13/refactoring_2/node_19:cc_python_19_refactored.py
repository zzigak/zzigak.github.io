from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n = int(input())
    parents = [int(input()) for _ in range(n-1)]
    edges = [(p-1, i-1) for i, p in enumerate(parents, start=2)]
    children = build_graph(n, edges, undirected=False)
    for node, ch in enumerate(children):
        if ch:
            leaf_children = sum(1 for c in ch if not children[c])
            if leaf_children < 3:
                print("No")
                return
    print("Yes")

if __name__ == "__main__":
    main()