from codebank import *

def main():
    _ = input()
    a = read_ints()
    rev, seeds = build_rev_graph_and_seeds(a)
    ans = bfs_from_seeds(rev, seeds)
    print(" ".join(map(str, ans)))

if __name__ == "__main__":
    main()