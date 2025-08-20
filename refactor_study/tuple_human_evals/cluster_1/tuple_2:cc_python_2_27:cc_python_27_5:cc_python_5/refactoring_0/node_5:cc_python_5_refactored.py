from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        a = int(data[idx]); b = int(data[idx + 1]); idx += 2
        if a == b:
            out.append("0")
            continue
        if a < b:
            a, b = b, a
        if a % b != 0:
            out.append("-1")
            continue
        ratio = a // b
        if not is_power_of_two(ratio):
            out.append("-1")
            continue
        diff = ratio.bit_length() - 1
        out.append(str(count_shift_ops(diff)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()