# ########## PROGRAM: node_7:cc_python_7 ##########

from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    m = int(data[0])
    s = ""
    sm = 0
    BAD = {"0011", "0101", "1110", "1111"}
    mod = 10**9 + 7
    idx = 1
    out = []
    for _ in range(m):
        s += data[idx]; idx += 1
        f = count_dp(s, BAD, mod)
        Z = compute_z(s[::-1])
        new = len(s) - max(Z)
        sm = (sm + sum(f[:new])) % mod
        out.append(str(sm))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()