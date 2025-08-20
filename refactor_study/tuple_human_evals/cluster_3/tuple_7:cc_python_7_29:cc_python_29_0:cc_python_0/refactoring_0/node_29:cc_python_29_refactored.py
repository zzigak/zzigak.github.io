from codebank import *

def main():
    n = int(input())
    adj = read_tree(n)
    v = list(map(int, input().split()))
    ans = compute_min_moves(adj, v)
    print(ans)

if __name__ == "__main__":
    main()