# ########## PROGRAM: node_21:cc_python_21 ##########

from codebank import *

def main():
    n = int(input())
    beaver = list(map(int, input().split()))
    adj = read_tree(n)
    start = int(input()) - 1
    print(max_beavers_eaten(beaver, adj, start))

if __name__ == "__main__":
    main()