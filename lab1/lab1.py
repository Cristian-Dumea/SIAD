# -------------------------------------------------------------------------------
# Name:         lab1.py
# Purpose:
# 
# Author:       Cristian-Petrisor Dumea
# Created:      2/24/2020
# Copyright:    (c) Cristian-Petrisor Dumea
#
# -------------------------------------------------------------------------------


# problema 1

# text = "Salut Siad!"
#
# numar1 = len(set(text))
# print(numar1)
#
# dict_freq = {}
# for caracter in text:
#     if caracter in dict_freq:
#         dict_freq[caracter] = dict_freq[caracter] + 1
#     else:
#         dict_freq[caracter] = 1
#
# print(dict_freq)

#
# rez = [(ana, bianca)
#        for bianca in range(1, 6)
#        if bianca != 1
#        for ana in range(1, 6)
#        if ana != 5
#        ]
#
# print(rez)

# problema 2

str_text = "Ana are un rotator cu capac "


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
    return dict_palindromes, list_palindromes


dict_result, list_result = find_palindromes(str_text)
print(dict_result)
print(list_result)
