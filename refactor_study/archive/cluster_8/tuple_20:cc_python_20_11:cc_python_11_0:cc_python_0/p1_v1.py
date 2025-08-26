# ########## PROGRAM: node_0:cc_python_0 ##########

from codebank import precompute_factorials, binomial

def main():
    MOD = 10**9 + 9
    n, w, b = map(int, input().split())
    factW, invW = precompute_factorials(w, MOD)
    factB, invB = precompute_factorials(b, MOD)

    ans = 0
    for black in range(max(1, n - w), min(n - 2, b) + 1):
        white_days = n - 1 - black
        ways_white = binomial(w - 1, white_days, factW, invW, MOD)
        ways_black = binomial(b - 1, black - 1, factB, invB, MOD)
        ans = (ans + white_days * ways_white * ways_black) % MOD

    ans = ans * factW[w] % MOD * factB[b] % MOD
    print(ans)

if __name__ == "__main__":
    main()