import sys
from codebank import *

def main():
    input = sys.stdin.readline
    m = int(input())
    seq = []
    sm = 0
    ans = []
    BAD = {
        (0,0,1,1), (0,1,0,1), (1,1,1,0), (1,1,1,1)
    }
    MOD = 10**9 + 7
    for _ in range(m):
        seq.append(int(input()))
        f = compute_dp(seq, BAD, MOD)
        start = new_substr_start(seq)
        sm = (sm + sum(f[:start])) % MOD
        ans.append(str(sm))
    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()