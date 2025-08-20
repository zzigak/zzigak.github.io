from codebank import *

def main():
    import sys
    s = sys.stdin.readline().strip()
    n = len(s)
    Z = zfunction(s)
    # prefix-max of Z for quick middle-occurrence check
    pm = [0]*n
    for i in range(1, n):
        pm[i] = pm[i-1] if pm[i-1] > Z[i] else Z[i]
    # try suffixes in descending length order
    for i in range(1, n):
        x = n - i
        # check suffix match and a middle occurrence before position i
        if Z[i] == x and i-1 >= 1 and pm[i-1] >= x:
            print(s[:x])
            return
    print("Just a legend")

if __name__ == "__main__":
    main()