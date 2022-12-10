from b_functions import *

if __name__ == "__main__":
    print("hi")

    for k, v in func_list.items():
        show_function(v, k, dim=1)
        show_function(v, k, dim=2)
