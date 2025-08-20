from codebank import *

def main():
    import sys
    s = sys.stdin.readline().strip()
    Z = z_function(s)
    borders = [Z[i] for i in range(len(s)) if i + Z[i] == len(s)]
    if not borders:
        print("Just a legend")
        return
    borders.sort(reverse=True)
    best = borders[0]
    if Z.count(best) >= 2 or max(Z) > best:
        print(s[:best])
    elif len(borders) > 1:
        print(s[:borders[1]])
    else:
        print("Just a legend")

if __name__ == "__main__":
    main()