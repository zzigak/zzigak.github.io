from codebank import dp_ways, z_function
import sys

def main():
    m = int(sys.stdin.readline())
    bad = {'0011', '0101', '1110', '1111'}
    MOD = 10**9 + 7
    sm = 0
    s = ''
    for _ in range(m):
        s += sys.stdin.readline().strip()
        f = dp_ways(s, bad, MOD)
        z_rev = z_function(s[::-1])
        max_z = max(z_rev)
        new = len(s) - max_z
        sm = (sm + sum(f[:new])) % MOD
        print(sm)

if __name__ == "__main__":
    main()