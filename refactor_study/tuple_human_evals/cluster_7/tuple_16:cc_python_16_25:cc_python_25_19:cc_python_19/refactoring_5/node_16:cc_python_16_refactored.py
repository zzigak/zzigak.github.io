from codebank import *

def main():
    import sys
    data = sys.stdin.readline
    n = int(data())
    ans, m = build_max_beauty_permutation(n)
    print(m)
    print(*ans)

if __name__ == "__main__":
    main()