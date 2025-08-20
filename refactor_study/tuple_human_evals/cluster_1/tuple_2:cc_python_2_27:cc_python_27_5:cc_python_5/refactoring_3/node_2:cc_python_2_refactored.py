from codebank import *

def main():
    a, b = map(int, input().split())
    e2_a, e3_a, e5_a, cof_a = get_235_info(a)
    e2_b, e3_b, e5_b, cof_b = get_235_info(b)
    if cof_a != cof_b:
        print(-1)
    else:
        print(abs(e2_a - e2_b) + abs(e3_a - e3_b) + abs(e5_a - e5_b))

if __name__ == "__main__":
    main()