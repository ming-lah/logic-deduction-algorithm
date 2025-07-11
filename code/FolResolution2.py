from MGU import MGU, term_substitution

def is_false(str):
    if str[0] == '~':
        return True
    else:
        return False

    
def use_substitution(str, substitution):
    """
    对公式进行替换
    """
    if str[0] == '~':
        tmp = str[1:]
        new_str = term_substitution(tmp, substitution)
        return '~' + new_str
    else:
        return term_substitution(str, substitution)

def str_MGU(str1, str2):
    """
    对可以归结的公式进行合一
    """
    if str1[0] == '~' and str2[0] != '~':
        new_str1 = str1[1:]
        new_str2 = str2
        return MGU(new_str1, new_str2)
    elif str1[0] != '~' and str2[0] == '~':
        new_str1 = str1
        new_str2 = str2[1:]
        return MGU(new_str1, new_str2)
    else:
        return None

def solve_clause(clause1, clause2, num1, num2):
    """
    两两归结
    """
    clause1_list = list(clause1)
    clause2_list = list(clause2)
    ans = []

    if len(clause1_list) == 1:
        clause = clause1_list[0]
        for i, list2 in enumerate(clause2_list):
            if is_false(clause) != is_false(list2):
                substitution = str_MGU(clause, list2)
                if substitution is not None:
                    new_clause = set(clause2_list) - {list2}
                    new_clause = {use_substitution(l, substitution) for l in new_clause}
                    label = f"R[{num1}a, {num2}{chr(ord('a')+i)}] {substitution}"
                    ans.append((label, frozenset(new_clause)))
    elif len(clause2_list) == 1:
        clause = clause2_list[0]
        for i, list1 in enumerate(clause1_list):
            if is_false(clause) != is_false(list1):
                substitution = str_MGU(list1, clause)
                if substitution is not None:
                    new_clause = set(clause1_list) - {list1}
                    new_clause = {use_substitution(l, substitution) for l in new_clause}
                    label = f"R[{num1}{chr(ord('a')+i)}, {num2}a] {substitution}"
                    ans.append((label, frozenset(new_clause)))
    else:
        for i, list1 in enumerate(clause1_list):
            for j, list2 in enumerate(clause2_list):
                if is_false(list1) != is_false(list2):
                    substitution = str_MGU(list1, list2)
                    if substitution is not None:
                        new_clause = set(clause1_list[:i] + clause1_list[i+1:] + clause2_list[:j] + clause2_list[j+1:])
                        new_substitution = {use_substitution(k, substitution) for k in new_clause}
                        label = f"R[{num1}{chr(ord('a')+i)}, {num2}{chr(ord('a')+j)}] {substitution}"
                        ans.append((label, frozenset(new_substitution)))
    return ans

def print_ans(messages, flag=None):
    """
    输出归结过程
    """
    print("归结过程：")
    for key in messages:
        clause, output = messages[key]
        clause_str = "(" + ", ".join(clause) + ")" if clause else "[]"
        if output == "1":
            print(f"{key} {clause_str}")
        else:
            print(f"{key}: {output} => {clause_str}")
        if flag is not None and key == flag:
            break

def issub(clause1, clause2):
    """
    用于判断是否是包含关系
    """
    return clause1.issubset(clause2)

def solve_prop(KB):
    """
    总实现函数
    """
    clauses= []
    messages = {}
    num = 1
    flag_set = set()
    for i in KB:
        clause = frozenset(i)
        clauses.append((num, clause)) # clause
        messages[num] = (clause, "1") # clause and output
        flag_set.add(clause) # flag
        num += 1
    
    while True:
        clauses.sort(key=lambda item: len(item[1]))
        n = len(clauses)
        new_clauses = []
        for i in range(n):
            for j in range(i+1, n):
                num1, clause1 = clauses[i]
                num2, clause2 = clauses[j]
                ans = solve_clause(clause1, clause2, num1, num2)
                for (output, new_cal) in ans:
                    if new_cal not in flag_set:
                        new_clauses.append((output, new_cal))
        if not new_clauses:
            print("无法退出新句子")
            print(messages)
            return messages
        # new fliter_function
        filtered_clause = []
        for output, clause in new_clauses:
            # new_clause include i
            flag = False
            for i in flag_set:
                if issub(i, clause):
                    flag = True
                    break
            if flag == True:
                continue
            # i include new_clause
            remove_set = set()
            for i in flag_set:
                if issub(clause, i):
                    remove_set.add(i)
            if remove_set:
                flag_set = flag_set - remove_set
                clauses = [(n_val, cl) for n_val, cl in clauses if cl not in remove_set]

            if clause not in flag_set:
                filtered_clause.append((output, clause))
                messages[num] = (clause, output)
                clauses.append((num, clause))
                flag_set.add(clause)
                num += 1

        for output, clause in filtered_clause:
            if len(clause) == 0:
                print_ans(messages)
                return messages



#  test： the KB is a list
def main():
    KB = [
        {"GradStudent(sue)"},
        {"~GradStudent(x)", "Student(x)"},
        {"~Student(x)", "HardWorker(x)"},
        {"~HardWorker(sue)"}
    ]
    
    solve_prop(KB)

if __name__ == '__main__':
    main()
