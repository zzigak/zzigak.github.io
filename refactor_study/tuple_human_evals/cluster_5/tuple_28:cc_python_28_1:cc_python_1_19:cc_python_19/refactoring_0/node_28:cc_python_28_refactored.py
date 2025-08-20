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
        nxt_s, nxt_l = X[-1], Y[-1]
        cand = c + nxt_s
        l = nxt_l + 1
        if l > 10:
            cand = trim_str(cand)
        if c == s[i+1] and cand > X[-2]:
            cand, l = X[-2], Y[-2]
        X.append(cand); Y.append(l)
    for i in range(n-1, -1, -1):
        print(Y[i], X[i])

if __name__ == "__main__":
    main()