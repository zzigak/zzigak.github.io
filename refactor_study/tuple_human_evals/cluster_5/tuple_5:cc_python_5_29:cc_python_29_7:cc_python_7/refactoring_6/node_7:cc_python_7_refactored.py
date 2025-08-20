from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    m = int(data[0])
    bits = list(map(int, data[1:]))
    s = []
    sm = 0
    ans = []
    MOD = 10**9+7
    BAD = {(0,0,1,1),(0,1,0,1),(1,1,1,0),(1,1,1,1)}
    for b in bits:
        s.append(b)
        f = update_dp(s, BAD, MOD)
        Z = z_function(s[::-1])
        new = len(s) - max(Z) if Z else len(s)
        sm = (sm + sum(f[:new])) % MOD
        ans.append(str(sm))
    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()