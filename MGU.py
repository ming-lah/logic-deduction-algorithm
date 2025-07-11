import string


def formular_solve(formula):
    """
    解析公式
    """

    if '(' not in formula or ')' not in formula:
        return (formula, [])
    
    formula = formula.strip()
    left_most_index = formula.find('(')
    right_most_index = formula.rfind(')')

    
    # if left_most_index == -1 or right_most_index == -1 or right_most_index != len(formula) - 1:
    #     return ("INVALID", formula)
    
    name = formula[:left_most_index].strip()
    parameter_str = formula[left_most_index + 1: right_most_index].strip()

    count = 0 
    args = []
    current_char = []
    for i in parameter_str:
        if i == '(':
            count += 1
            current_char.append(i)
        elif i == ')':
            count -= 1
            current_char.append(i)
        elif i == ',' and count == 0:
            arg = ''.join(current_char).strip()
            if arg != "":
                args.append(arg)
            current_char = []
        else:
            current_char.append(i)

    if current_char:
        arg = ''.join(current_char).strip()
        if arg != "":
            args.append(arg)

    # if count != 0:
    #     return ("INVALID", formula)

    return (name, args)




def term_substitution(term, substitution):
    """
    递归替换
    """
    name, args = formular_solve(term)

    if not args:
        if term in substitution:
            return term_substitution(substitution[term], substitution) # 
        else:
            return term
    
    new_args = []
    for i in args:
        new_args.append(term_substitution(i, substitution))
    return f"{name}({','.join(new_args)})"

def check(var, term ,substitution):
    """
    检查是否出现过变量
    """
    term_change = term_substitution(term, substitution)

    if term_change == var:
        return True
    name, args = formular_solve(term_change)
    for i in args:
        if i == var or check(var, i, substitution):
            return True
    return False

def is_variable(var):
    list = {'a','b','x','xx','y','yy','z','zz','u','uu','w','v'}
    return var in list

def change_var(var, x, substitution):
    """
    替换变量
    """
    if not is_variable(var):
        if var == x:
            return substitution
        else:
            return None

    if var in substitution:
        return change(substitution[var], x, substitution)
    elif x in substitution:
        return change(var, substitution[x], substitution)
    else:
        if check(var, x, substitution):
            return None
        substitution[var] = x
        return substitution


def change(t1, t2, substitution):
    """
    合一
    """
    t1_change = term_substitution(t1, substitution)
    t2_change = term_substitution(t2, substitution)

    if t1_change == t2_change:
        return substitution
    
    name1, args1 = formular_solve(t1_change)
    name2, args2 = formular_solve(t2_change)

    if args1 == [] and args2 == []:
        if t1_change != t2_change:
            if is_variable(t1_change):
                return change_var(t1_change, t2_change, substitution)
            elif is_variable(t2_change):
                return change_var(t2_change, t1_change, substitution)
            else:
                return None
        else:
            return substitution
    
    if args1 == []:
        if is_variable(t1_change):
            return change_var(t1_change, t2_change, substitution)
        else:
            return None
    
    if args2 == []:
        if is_variable(t2_change):
            return change_var(t2_change, t1_change, substitution)
        else:
            return None
    
    if name1 == name2 and len(args1) == len(args2):
        for i1, i2 in zip(args1, args2):
            substitution = change(i1, i2, substitution)
            if substitution is None:
                return None
    else:
        return None
    
    return substitution



def MGU(term1, term2):
    """
    总的合一
    """
    name1, args1 = formular_solve(term1)
    name2, args2 = formular_solve(term2)

    if args1 == [] and args2 == []:
        return change(term1, term2, {})

    if name1 != name2:
        return None

    substitution = {}

    if len(args1) == len(args2):
        for i1, i2 in zip(args1, args2):
            substitution = change(i1, i2, substitution)
            if substitution is None:
                return None
    else:
        return None
    
    return substitution


if __name__ == "__main__":

    # test for formular_solve
    print("------test1------")
    formular_str = "P(a, b, f(x))"
    result = formular_solve(formular_str)
    print(result)
    print("------end------")
    print("\n")

    # test for MGU
    print("-----test2-----")
    ex1 = MGU("P(x,a)", "P(b,yy)")
    print("MGU(P(x,a), P(b,yy)) =", ex1)
    
    ex2 = MGU("P(a,xx,f(g(yy)))", "P(zz,f(zz),f(uu))")
    print("MGU(P(a,xx,f(g((yy))), P(zz,f(zz),f(uu))) =", ex2)
    print("------end------")



