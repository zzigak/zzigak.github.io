from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:]))
    counts = count_divisors(arr)
    mod = 10**9 + 7
    print(mobius_count(counts, mod))

if __name__ == "__main__":
    main()