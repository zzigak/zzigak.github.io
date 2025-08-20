from codebank import *

def main():
    n = int(input())
    a = list(read_ints())
    adj_rev, sources, ans = build_rev_graph_and_sources(a)
    res = multi_source_bfs(adj_rev, sources, ans)
    print(" ".join(map(str, res)))

if __name__ == "__main__":
    main()