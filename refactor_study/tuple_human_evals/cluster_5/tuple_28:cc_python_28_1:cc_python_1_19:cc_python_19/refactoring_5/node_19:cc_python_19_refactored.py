from codebank import *

def main():
    MOD = 10**9+7
    s = read_str()
    count_a = 0
    result = 0
    for ch in s:
        if ch == 'a':
            count_a = (count_a*2 + 1) % MOD
        else:
            result = (result + count_a) % MOD
    print(result)

if __name__ == "__main__":
    main()