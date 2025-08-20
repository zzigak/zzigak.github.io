from codebank import *

def main():
    s = read_str()
    MOD = 10**9 + 7
    cnta = 0
    ans = 0
    for ch in s:
        if ch == 'a':
            cnta = (cnta * 2 + 1) % MOD
        else:  # 'b'
            ans = (ans + cnta) % MOD
    print(ans)

if __name__ == "__main__":
    main()