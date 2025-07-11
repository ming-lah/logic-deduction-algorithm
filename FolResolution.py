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
    clause1 = list(clause1)
    clause2 = list(clause2)
    ans = []
    for i, list1 in enumerate(clause1):
        for j, list2 in enumerate(clause2):
            if is_false(list1) != is_false(list2):
                substitution = str_MGU(list1, list2)
                if substitution is not None:
                    new_clause = set(clause1[:i] + clause1[i+1:] + clause2[:j] + clause2[j+1:])
                    new_substitution = {use_substitution(k, substitution) for k in new_clause}
                    label = f"R[{num1}{chr(ord('a')+i)}, {num2}{chr(ord('a')+j)}] {substitution}"
                    ans.append((label, frozenset(new_substitution)))
    return ans


def print_ans(messages, flag = None):
    """
    输出函数
    """
    print("归结过程：")
    for i in (messages.keys()):
        clause, output = messages[i]
        clause_str = "(" + ", ".join(clause) + ")" if clause else "[]"

        if output == "1":
            print(f"{i} {clause_str}")
        else:
            print(f"{i}: {output} => {clause_str}")
        if flag is not None and i == flag:
            break



def solve_prop(KB):
    """
    总实现函数
    """
    clauses= []
    messages = {}
    num = 1
    flag_set = set()
    for i in KB:
        if isinstance(i, (tuple, list)):
            clause = frozenset(i)
        else:
            clause = frozenset((i,))
        clauses.append((num, clause)) # clause
        messages[num] = (clause, "1") # clause and output
        flag_set.add(clause) # flag
        num += 1
    
    while True:
        n = len(clauses)
        new_clauses = []
        for i in range(n):
            for j in range(i+1, n):
                num1, clause1 = clauses[i]
                num2, clause2 = clauses[j]
                ans = solve_clause(clause1, clause2, num1, num2)
                for (output, new_cal) in ans:
                    if new_cal not in flag_set:
                        messages[num] = (new_cal, output)
                        if len(new_cal) == 0:
                            print_ans(messages)
                            return messages
                        new_clauses.append((num, new_cal))
                        flag_set.add(new_cal)
                        num += 1
        if not new_clauses:
            print("无法退出新句子")
            print(messages)
            return messages
        clauses.extend(new_clauses)



# def main():
#     KB = {
#         ("GradStudent(sue)"),
#         ("~GradStudent(x)", "Student(x)"),
#         ("~Student(x)", "HardWorker(x)"),
#         ("~HardWorker(sue)")
#     }
    
#     solve_prop(KB)

# if __name__ == '__main__':
#     main()
