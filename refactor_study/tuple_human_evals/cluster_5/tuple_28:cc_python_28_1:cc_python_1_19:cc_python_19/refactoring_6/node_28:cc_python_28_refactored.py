from codebank import *

def main():
    s = read_str()
    n = len(s)
    if n == 1:
        print(1, s)
        return
    X, Y = [], []
    # suffix of length 1
    X.append(s[-1]); Y.append(1)
    # suffix of length 2
    if s[-2] != s[-1]:
        X.append(s[-2] + s[-1]); Y.append(2)
    else:
        X.append(""); Y.append(0)
    # build DP for suffixes of increasing length
    for i in range(n - 3, -1, -1):
        c = s[i]
        raw = c + X[-1]
        ng = Y[-1] + 1
        # truncate only if new length > 10
        k1 = truncate_str(raw) if ng > 10 else raw
        # if we can remove pair (i,i+1), compare with skipping
        if c == s[i + 1] and k1 > X[-2]:
            k1 = X[-2]; ng = Y[-2]
        X.append(k1); Y.append(ng)
    # output from longest suffix to shortest
    for length, out in zip(reversed(Y), reversed(X)):
        print(length, out)

if __name__ == "__main__":
    main()