from codebank import *

def main():
    n = int(input())
    total, perm = max_beauty_permutation(n)
    print(total)
    print(*perm)

if __name__ == "__main__":
    main()