from codebank import *

def main():
    import sys
    s = sys.stdin.readline().strip()
    n = len(s)
    Z = z_function(s)
    borders = [Z[i] for i in range(1, n) if i + Z[i] == n]
    if not borders:
        print("Just a legend")
        return
    for l in sorted(borders, reverse=True):
        # check for an interior occurrence: start j in [1..n-l-1]
        if any(Z[j] >= l for j in range(1, n - l)):
            print(s[:l])
            return
    print("Just a legend")

if __name__ == "__main__":
    main()