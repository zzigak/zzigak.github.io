from codebank import *

def main():
    import sys
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    for _ in range(t):
        a = int(data[idx]); b = int(data[idx+1])
        idx += 2
        out.append(str(min_shifts(a, b)))
    print("\n".join(out))

if __name__ == "__main__":
    main()