from codebank import *

def main():
    import sys
    n = int(sys.stdin.readline())
    ans = [-1] * (n + 1)
    for i in range(n, -1, -1):
        if ans[i] < 0:
            mask = all_ones_mask(i)
            j = i ^ mask
            ans[i] = j
            ans[j] = i
    total = 0
    for i, v in enumerate(ans):
        total += i ^ v
    out = sys.stdout
    out.write(str(total) + "\n")
    out.write(" ".join(map(str, ans)))

if __name__ == "__main__":
    main()