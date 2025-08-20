from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    t = int(data[0])
    res = []
    idx = 1
    for _ in range(t):
        a = int(data[idx]); b = int(data[idx+1]); idx += 2
        if a == b:
            res.append("0"); continue
        big, small = max(a, b), min(a, b)
        if big % small != 0:
            res.append("-1"); continue
        r = big // small
        if not is_power_of_two(r):
            res.append("-1"); continue
        e = r.bit_length() - 1
        res.append(str(min_shifts_ops(e)))
    sys.stdout.write("\n".join(res))

if __name__ == "__main__":
    main()