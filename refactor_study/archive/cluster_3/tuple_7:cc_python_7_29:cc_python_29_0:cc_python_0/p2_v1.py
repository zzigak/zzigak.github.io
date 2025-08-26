# ########## PROGRAM: node_29:cc_python_29 ##########

from codebank import *

def main():
    import sys
    data = sys.stdin
    n = int(data.readline())
    adj = read_tree(n, offset=1)
    raw_v = list(map(int, data.readline().split()))
    v = [0] + raw_v
    res = compute_min_moves(v, adj, root=1)
    print(res)

if __name__ == "__main__":
    main()