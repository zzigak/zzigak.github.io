from codebank import *

def main():
    s = read_str()
    mod = 10**9 + 7
    count_a = 0
    res = 0
    for ch in s:
        if ch == 'a':
            count_a = (count_a * 2 + 1) % mod
        else:  # ch == 'b'
            res = (res + count_a) % mod
    print(res)

if __name__ == "__main__":
    main()