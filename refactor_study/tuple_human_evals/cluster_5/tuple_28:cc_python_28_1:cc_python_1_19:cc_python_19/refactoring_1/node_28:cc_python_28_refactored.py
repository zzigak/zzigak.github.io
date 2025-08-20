from codebank import *

def main():
    s = read_str()
    n = len(s)
    if n == 1:
        print(1, s)
        return
    X = [s[-1], "" if s[-2] == s[-1] else s[-2] + s[-1]]
    Y = [1, 0 if s[-2] == s[-1] else 2]
    for i in range(n - 3, -1, -1):
        c = s[i]
        k1 = c + X[-1]
        ng = Y[-1] + 1
        k1 = truncate(k1)
        if c == s[i + 1] and k1 > X[-2]:
            k1 = X[-2]
            ng = Y[-2]
        X.append(k1)
        Y.append(ng)
    for i in range(n - 1, -1, -1):
        print(Y[i], X[i])

if __name__ == "__main__":
    main()