from codebank import *

def main():
    s = read_str()
    lengths, strs = dp_compute_suffixes(s)
    for l, st in zip(lengths, strs):
        print(l, st)

if __name__ == "__main__":
    main()