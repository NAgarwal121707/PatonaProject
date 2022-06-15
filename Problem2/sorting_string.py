def sort_string():
    user_input = input("Enter string need to be sorted: ")
    print("String to be sorted is", user_input)
    sorted_string = ''.join(sorted(user_input.strip()))
    print("After sorting string is", sorted_string)
    return sorted_string


sort_string()


