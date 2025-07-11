from FolResolution import solve_prop as solve_prop1 # 未优化的算法，传入参数KB为set
from FolResolution2 import solve_prop as solve_prop2# 优化后的算法，传入参数KB为list



if __name__ == '__main__':
    """
    下面给出两个测试，分别对应未优化的算法以及优化的算法
    对于未优化的算法:
    输出的归结过程中的初始KB的子句的每一文字可能和输入的顺序不一样
    同时输出归结过程的子句顺序也和初始的不一样
    这是因为使用了set存放子句集以及子句的每一个文字用于判断是否出现重复
    从归结的结果来看，归结推理的过程是正确的
    对于优化的算法:
    只是输出的子句中的文字和输入的可能不同，保证归结推理的正确性
    """
    #未优化算法的对应测试

    print("------未优化的归结推理-------")
    KB1 = {
        ("GradStudent(sue)"),
        ("~GradStudent(x)", "Student(x)"),
        ("~Student(x)", "HardWorker(x)"),
        ("~HardWorker(sue)")
    }
    
    result1 = solve_prop1(KB1)

    print("\n")
    print("--------------------")
    print("\n")

    KB2 = {
        ("A(tony)"),
        ("A(mike)"),
        ("A(john)"),
        ("L(tony, rain)"),
        ("L(tony, snow)"),
        ("~A(x)", "S(x)", "C(x)"),
        ("~C(y)", "~L(y, rain)"),
        ("L(z, snow)", "~S(z)"),
        ("~L(tony, u)", "~L(mike, u)"),
        ("L(tony, v)", "L(mike, v)"),
        ("~A(w)", "~C(w)", "S(w)")
    }

    result2 = solve_prop1(KB2)

    print("\n")
    print("--------------------")
    print("\n")

    KB3 = {
        ("On(tony, mike)"),
        ("On(mike, john)"),
        ("Green(tony)"),
        ("~Green(john)"),
        ("~On(xx, yy)", "~Green(xx)", "Green(yy)")
    }
    result3 = solve_prop1(KB3)

    # 优化算法的对应测试
    print("\n")
    print("------优化的归结推理------")
    print("\n")

    KB1 = [
        {"GradStudent(sue)"},
        {"~GradStudent(x)", "Student(x)"},
        {"~Student(x)", "HardWorker(x)"},
        {"~HardWorker(sue)"}
    ]
    
    result1 = solve_prop2(KB1)

    print("\n")
    print("--------------------")
    print("\n")

    KB2 = [
        {"A(tony)"},
        {"A(mike)"},
        {"A(john)"},
        {"L(tony, rain)"},
        {"L(tony, snow)"},
        {"~A(x)", "S(x)", "C(x)"},
        {"~C(y)", "~L(y, rain)"},
        {"L(z, snow)", "~S(z)"},
        {"~L(tony, u)", "~L(mike, u)"},
        {"L(tony, v)", "L(mike, v)"},
        {"~A(w)", "~C(w)", "S(w)"}
    ]

    result2 = solve_prop2(KB2)

    print("\n")
    print("--------------------")
    print("\n")

    KB3 = [
        {"On(tony, mike)"},
        {"On(mike, john)"},
        {"Green(tony)"},
        {"~Green(john)"},
        {"~On(xx, yy)", "~Green(xx)", "Green(yy)"}
    ]
    result3 = solve_prop2(KB3)






