from codebank import *

def main():
    s = read_str()
    N = len(s)
    if N == 1:
        print(1, s)
        return
    X = [""] * N
    Y = [0] * N
    X[N-1], Y[N-1] = s[N-1], 1
    if s[N-2] != s[N-1]:
        X[N-2], Y[N-2] = s[N-2] + X[N-1], 2
    else:
        X[N-2], Y[N-2] = "", 0
    for i in range(N-3, -1, -1):
        c = s[i]
        add = c + X[i+1]
        ln = Y[i+1] + 1
        if ln > 10:
            add = trunc(add)
        if c == s[i+1] and add > X[i+2]:
            X[i], Y[i] = X[i+2], Y[i+2]
        else:
            X[i], Y[i] = add, ln
    for i in range(N):
        print(Y[i], X[i])

if __name__ == "__main__":
    main()