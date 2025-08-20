from codebank import *

def main():
    s = read_str()
    n = len(s)
    X = [''] * n
    Y = [0] * n
    if n >= 1:
        X[n-1] = s[-1]
        Y[n-1] = 1
    if n >= 2:
        if s[-2] != s[-1]:
            X[n-2] = s[-2] + s[-1]
            Y[n-2] = 2
        else:
            X[n-2], Y[n-2] = "", 0
    for i in range(n-3, -1, -1):
        cand = s[i] + X[i+1]
        length = Y[i+1] + 1
        if length > 10:
            cand = truncate_string(cand)
        # if we can pair s[i] with s[i+1], consider skipping both
        if s[i] == s[i+1] and X[i+2] < cand:
            X[i], Y[i] = X[i+2], Y[i+2]
        else:
            X[i], Y[i] = cand, length
    for i in range(n):
        print(Y[i], X[i])

if __name__ == "__main__":
    main()