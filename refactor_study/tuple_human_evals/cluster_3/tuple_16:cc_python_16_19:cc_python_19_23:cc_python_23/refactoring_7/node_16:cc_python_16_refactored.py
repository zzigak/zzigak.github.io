from codebank import *
import sys
input = sys.stdin.readline

def main():
    n, k = map(int, input().split())
    adj = read_tree(n)
    depth, sizes = compute_depth_and_subtree(adj, 0)
    scores = [sizes[i] - depth[i] for i in range(n)]
    scores.sort(reverse=True)
    print(sum(scores[:n-k]))

if __name__ == "__main__":
    main()