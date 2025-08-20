# ########## PROGRAM: node_0:cc_python_0 ##########

from codebank import *

def main():
    import sys
    data = sys.stdin
    n = int(data.readline())
    b_list = list(map(int, data.readline().split()))
    a_list = list(map(int, data.readline().split()))
    diff = [0]*(n+1)
    for i in range(1, n+1):
        diff[i] = b_list[i-1] - a_list[i-1]
    parent = [0]*(n+1); k=[0]*(n+1)
    for i in range(2, n+1):
        x, ki = map(int, data.readline().split())
        parent[i] = x; k[i] = ki
    ok = propagate_diff(diff, parent, k)
    print("YES" if ok else "NO")

if __name__ == "__main__":
    main()