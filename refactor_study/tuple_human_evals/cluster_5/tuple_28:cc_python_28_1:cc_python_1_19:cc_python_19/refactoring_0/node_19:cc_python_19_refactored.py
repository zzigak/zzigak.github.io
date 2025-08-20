from codebank import *

def main():
    mod = 10**9 + 7
    s = read_str()
    cnt_a = 0
    res = 0
    for ch in s:
        cnt_a, res = process_char(ch, cnt_a, res, mod)
    print(res)

if __name__ == "__main__":
    main()