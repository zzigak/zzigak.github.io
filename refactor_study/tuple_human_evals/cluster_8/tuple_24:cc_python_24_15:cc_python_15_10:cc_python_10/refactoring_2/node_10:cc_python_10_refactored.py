from codebank import *
import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])
    print(solve_query3(N, M, MOD))

if __name__ == "__main__":
    main()