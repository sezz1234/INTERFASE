import tkinter as tk
from typing import List
import math

def algorithm_lz77(input_user: str, buffer_size: int, dictionary_size: int) -> List[List[str]]:
    output_model: List[List[str]] = []
    index_char = 0
    while index_char < len(input_user):
        best_length = 0
        best_offset = 0
        next_char = ""
        max_offset = min(index_char, dictionary_size)
        max_length = min(len(input_user) - index_char, buffer_size)
        for offset in range(1, max_offset + 1):
            for length in range(1, max_length + 1):
                string_window = input_user[index_char - offset:index_char - offset + length]
                string_buffer = input_user[index_char:index_char + length]
                if string_window == string_buffer and length > best_length:
                    best_length = length
                    best_offset = (offset - dictionary_size) * (-1)
                    if index_char + length < len(input_user):
                        next_char = input_user[index_char + length]
        if index_char == len(input_user) - 1:
            output_model.append([input_user[max(0, index_char - dictionary_size):index_char],
                                 input_user[index_char:min(index_char + buffer_size, len(input_user))],
                                 "<0,0," + input_user[index_char] + ">"])
        else:
            output_model.append([input_user[max(0, index_char - dictionary_size):index_char],
                                 input_user[index_char:min(index_char + buffer_size, len(input_user))],
                                 "<" + str(best_offset) + "," + str(best_length) + "," + (next_char if best_length > 0 else input_user[index_char]) + ">"])
        index_char += best_length + 1
    for item in output_model:
        item[1] = item[1][:buffer_size].ljust(buffer_size)
        item[0] = item[0][-dictionary_size:].rjust(dictionary_size)
    return output_model

def algorithm_lz78(input_user: str, dictionary_size: int) -> List[List[str]]:
    dictionary = [""]
    frequency = {}
    output_model: List[List[str]] = [["''", "", "0"]]
    i = 0
    while i < len(input_user):
        window_symbols = input_user[i]
        index = next((idx for idx, val in enumerate(dictionary) if val == window_symbols), len(dictionary))
        while index != len(dictionary) and i < len(input_user) - 1:
            i += 1
            window_symbols += input_user[i]
            index = next((idx for idx, val in enumerate(dictionary) if val == window_symbols), len(dictionary))
        if index == len(dictionary):
            code = f"<{dictionary.index(window_symbols[:-1])}, '{window_symbols[-1]}'>"
            output_model.append([f"'{window_symbols}'", code, str(len(dictionary))])
            if len(dictionary) == dictionary_size:
                last_used = min(frequency, key=frequency.get)
                dictionary.remove(last_used)
                del frequency[last_used]
            dictionary.append(window_symbols)
            frequency[window_symbols] = 1
        else:
            frequency[window_symbols] = frequency.get(window_symbols, 0) + 1
        i += 1
    check_last_two_symbols = input_user[-2:]
    last_item_output_model = dictionary[-1]
    if check_last_two_symbols not in last_item_output_model:
        last_symbol = input_user[-1]
        code = f"<{dictionary.index('')}, '{last_symbol}'>"
        output_model.append([f"'{last_symbol}'", code, str(len(dictionary))])
    return output_model

def algorithm_lzss(input_user: str, buffer_size: int, dictionary_size: int) -> List[List[str]]:
    output_model: List[List[str]] = []
    dictionary = ""
    buffer_str = input_user[:min(buffer_size, len(input_user))]
    input_user = input_user[len(buffer_str):]
    while buffer_str:
        offset = 0
        length = 0
        for i in range(1, len(buffer_str) + 1):
            sub_str = buffer_str[:i]
            position = dictionary.rfind(sub_str)
            if position != -1:
                offset = dictionary_size - len(dictionary) + position
                length = len(sub_str)
            else:
                break
        if length > 0:
            code = f"1<{offset},{length}>"
            code_length = int(math.log2(dictionary_size)) + int(math.log2(buffer_size)) + 2
        else:
            code = f"0'{buffer_str[0]}'"
            code_length = 9
        output_model.append([dictionary, buffer_str, code, str(code_length)])
        shift_size = max(length, 1)
        dictionary += buffer_str[:shift_size]
        if len(dictionary) > dictionary_size:
            dictionary = dictionary[-dictionary_size:]
        buffer_str = buffer_str[shift_size:]
        if len(buffer_str) < buffer_size and input_user:
            add_size = min(buffer_size - len(buffer_str), len(input_user))
            buffer_str += input_user[:add_size]
            input_user = input_user[add_size:]
    return output_model


def display_results():
    input_user = entry.get()
    dictionary_size = int(entry_dict_size.get())
    buffer_size = int(entry_buffer_size.get())

    result_lz77 = algorithm_lz77(input_user, buffer_size, dictionary_size)
    result_lz78 = algorithm_lz78(input_user, dictionary_size)
    result_lzss = algorithm_lzss(input_user, buffer_size, dictionary_size)

    for item in result_lz77:
        label_result_lz77 = tk.Label(root, text=f"{item[0]}  {item[1]}  {item[2]}")
        label_result_lz77.pack()


    for item in result_lz78:
        label_result_lz78 = tk.Label(root, text=f"{item[0]}  {item[1]}  {item[2]}")
        label_result_lz78.pack()

    for item in result_lzss:
        label_result_lzss = tk.Label(root, text=f"{item[0]}  {item[1]}  {item[2]}  {item[3]}")
        label_result_lzss.pack()


root = tk.Tk()

label_input = tk.Label(root, text="Введите фразу:")
label_input.pack()
entry = tk.Entry(root)
entry.pack()

label_dict_size = tk.Label(root, text="Введите размер словаря (для всех методов):")
label_dict_size.pack()
entry_dict_size = tk.Entry(root)
entry_dict_size.pack()

label_buffer_size = tk.Label(root, text="Введите размер буфера (для LZ77 и LZSS):")
label_buffer_size.pack()
entry_buffer_size = tk.Entry(root)
entry_buffer_size.pack()

button = tk.Button(root, text="Показать результаты", command=display_results)
button.pack()

root.mainloop()