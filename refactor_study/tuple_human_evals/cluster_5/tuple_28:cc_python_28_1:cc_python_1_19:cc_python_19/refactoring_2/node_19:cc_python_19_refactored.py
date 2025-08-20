from codebank import *

def main():
    s = read_str()
    MOD = 10**9 + 7
    cnt = 0
    res = 0
    for ch in s:
        if ch == 'a':
            cnt = (cnt * 2 + 1) % MOD
        else:  # ch == 'b'
            res = (res + cnt) % MOD
    print(res)

if __name__ == "__main__":
    main()