from codebank import *

def main():
    s = read_str()
    n = len(s)
    if n == 1:
        print(1, s)
        return
    X, Y = [], []
    # base cases for last two suffixes
    X.append(s[-1]); Y.append(1)
    if s[-2] != s[-1]:
        X.append(s[-2]+s[-1]); Y.append(2)
    else:
        X.append(''); Y.append(0)
    # DP from i=n-3 down to 0
    for i in range(n-3, -1, -1):
        c = s[i]
        k1 = c + X[-1]
        ng = Y[-1] + 1
        k1 = truncate_str(k1)
        if c == s[i+1] and k1 > X[-2]:
            k1, ng = X[-2], Y[-2]
        X.append(k1); Y.append(ng)
    # output for each suffix
    for i in range(n-1, -1, -1):
        print(Y[i], X[i])

if __name__ == "__main__":
    main()