from codebank import *

def main():
    import sys
    n = int(sys.stdin.readline())
    fin, ans = compute_beauty_permutation(n)
    print(fin)
    print(*ans)

if __name__ == "__main__":
    main()