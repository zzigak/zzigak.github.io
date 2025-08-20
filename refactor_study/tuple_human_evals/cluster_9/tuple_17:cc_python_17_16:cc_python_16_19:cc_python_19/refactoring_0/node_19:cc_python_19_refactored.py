from codebank import *
import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))
    go, sources, dist = build_reverse_graph_for_parity(a)
    ans = multi_source_bfs(go, sources, dist)
    print(" ".join(map(str, ans)))

if __name__ == "__main__":
    main()