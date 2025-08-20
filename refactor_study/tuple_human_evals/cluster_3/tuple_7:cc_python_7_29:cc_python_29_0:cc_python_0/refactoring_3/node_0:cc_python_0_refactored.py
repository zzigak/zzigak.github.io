from codebank import *

def main():
    n = int(input())
    b = list(read_ints())
    a = list(read_ints())
    parents = [-1]*n
    ks = [1]*n
    for i in range(n-1):
        x, k = read_ints()
        parents[i+1] = x-1
        ks[i+1] = k
    print("YES" if can_satisfy(b, a, parents, ks) else "NO")

if __name__ == "__main__":
    main()