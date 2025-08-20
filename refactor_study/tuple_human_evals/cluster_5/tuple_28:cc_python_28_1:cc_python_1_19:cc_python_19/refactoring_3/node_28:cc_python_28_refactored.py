from codebank import *

def main():
    s = read_str()
    for length, rep in compute_lex_min_suffix(s):
        print(length, rep)

if __name__ == "__main__":
    main()