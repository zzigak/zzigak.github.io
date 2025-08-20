from codebank import *

def main():
    n = int(input())
    ans = pair_complement_permutation(n)
    m = compute_beauty(ans)
    print(m)
    print(*ans)

if __name__ == "__main__":
    main()