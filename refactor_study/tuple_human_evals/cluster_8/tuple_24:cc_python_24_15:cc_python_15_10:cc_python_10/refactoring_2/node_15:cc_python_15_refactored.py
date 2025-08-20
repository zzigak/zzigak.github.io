from codebank import *
import sys

def main():
    n = int(sys.stdin.read())
    print(solve_query2(n, 10**9 + 7))

if __name__ == "__main__":
    main()