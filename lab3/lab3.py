def check_palindrome(str_palindrome):
    int_len = len(str_palindrome) - 1
    for int_i in range(int(int_len)):
        if str_palindrome[int_i] != str_palindrome[int_len - int_i]:
            return 0
    return 1


def find_palindromes(str_phrase):
    dict_palindromes = {}
    list_palindromes = []
    int_len = len(str_phrase)
    for int_i in range(0, int_len - 1, 1):
        for int_j in range(int_i, int_len, 1):
            str_maybe_palindrome = str_phrase[int_i:int_j:1]
            b_palindrome_flag = check_palindrome(str_maybe_palindrome)
            if b_palindrome_flag == 1:
                dict_palindromes[len(str_maybe_palindrome)] = str_maybe_palindrome
                list_palindromes.append(str_maybe_palindrome)
            else:
                break
    return dict_palindromes, list_palindromes


def main():
    with open("pi_1m.txt", "r") as f:
        str_text = f.read()
    dict_result, _ = find_palindromes(str_text)
    print(dict_result)


if __name__ == "__main__":
    main()
