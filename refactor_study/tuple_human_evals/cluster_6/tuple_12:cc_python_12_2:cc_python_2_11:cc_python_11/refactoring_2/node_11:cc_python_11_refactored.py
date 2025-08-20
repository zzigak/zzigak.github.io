from codebank import *

def main():
    k, n, m = read_ints()
    a_list = read_ints()
    ops = []
    for idx in range(1, n + 1):
        t, i, b = read_ints()
        ops.append((t, i, b, idx))
    list_by_skill = classify_operations(k, ops)
    for skill_ops in list_by_skill:
        for lst in skill_ops:
            lst.sort(key=lambda x: x[0], reverse=True)
    op_candidates = build_operation_candidates(a_list, list_by_skill)
    selected = select_top_indices(op_candidates, m)
    result = flatten_selected_ops(list_by_skill, selected)
    print(len(result))
    if result:
        print(*result)

if __name__ == "__main__":
    main()