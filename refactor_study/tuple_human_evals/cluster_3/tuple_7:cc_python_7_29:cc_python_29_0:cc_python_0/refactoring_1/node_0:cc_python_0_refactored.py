from codebank import read_ints

def main():
    n = int(input())
    b = list(map(int, input().split()))
    a = list(map(int, input().split()))
    x = [0] * (n + 1)
    k = [0] * (n + 1)
    for i in range(2, n + 1):
        xi, ki = read_ints()
        x[i] = xi
        k[i] = ki
    diff = [0] * (n + 1)
    for i in range(1, n + 1):
        diff[i] = b[i - 1] - a[i - 1]
    for i in range(n, 1, -1):
        p = x[i]
        if diff[i] >= 0:
            diff[p] += diff[i]
        else:
            diff[p] += diff[i] * k[i]
    print("YES" if diff[1] >= 0 else "NO")

if __name__ == "__main__":
    main()