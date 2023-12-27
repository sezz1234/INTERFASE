import tkinter as tk


class Node:
    def __init__(self, sym, pro):
        self.sym = sym
        self.pro = pro
        self.arr = []
        self.top = -1


def shannon(l, h, p):
    pack1, pack2, diff1, diff2 = 0, 0, 0, 0
    i, d, k, j = 0, 0, 0, 0

    if (l + 1) == h or l == h or l > h:
        if l == h or l > h:
            return
        p[h].arr.append(1)
        p[l].arr.append(0)
        return
    else:
        for i in range(l, h + 1):
            pack1 += p[i].pro

        pack2 = p[h].pro
        diff1 = abs(pack1 - pack2)

        j = 2

        while j != h - l + 1:
            k = h - j
            pack1 = pack2 = 0

            for i in range(l, k + 1):
                pack1 += p[i].pro

            for i in range(h, k, -1):
                pack2 += p[i].pro

            diff2 = abs(pack1 - pack2)

            if diff2 >= diff1:
                break

            diff1 = diff2
            j += 1

        k += 1

        for i in range(l, k):
            p[i].arr.append(0)

        for i in range(k, h + 1):
            p[i].arr.append(1)

        shannon(l, k - 1, p)
        shannon(k, h, p)


def sort_by_probability(n, p):
    for j in range(1, n):
        for i in range(0, n - 1):
            if p[i].pro > p[i + 1].pro:
                temp = p[i]
                p[i] = p[i + 1]
                p[i + 1] = temp



def huffman(n, p):
    temp = 1
    print("\n\nМетод Хаффмена\nСимвол\tВероятность\tКод")

    print(f"\n{p[n-1].sym}\t{p[n-1].pro}\t\t0")

    for i in range(n - 2, 0, -1):
        print(f"\n{p[i].sym}\t{p[i].pro:.2f}\t\t{'1' * temp}0")
        temp += 1

    print(f"\n{p[0].sym}\t{p[0].pro}\t\t{'1' * (n - 1)}")



def display_in_text_box(text_box, n, symbols, prob_list, p_shannon, p_huffman):
    text_box.insert(tk.END, "\nМетод Шеннона-Фано\nСимвол\tВероятность\tКод\n")
    for i in range(n):
        text_box.insert(tk.END,
                        f"\n{symbols[i]}\t{prob_list[i]:.2f}\t\t{''.join(map(str, p_shannon[i].arr))}")

    text_box.insert(tk.END, "\n\nМетод Хаффмена\nСимвол\tВероятность\tКод\n")
    temp = 1
    text_box.insert(tk.END, f"\n{symbols[n - 1]}\t{prob_list[n - 1]}\t\t0")

    for i in range(n - 2, 0, -1):
        text_box.insert(tk.END, f"\n{symbols[i]}\t{prob_list[i]:.2f}\t\t{'1' * temp}0")
        temp += 1

    text_box.insert(tk.END, f"\n{symbols[0]}\t{prob_list[0]}\t\t{'1' * (n - 1)}")


def main(n, symbols, method, prob_list, text_box):
    p_shannon = []
    p_huffman = []

    for i in range(n):
        sym = symbols[i]
        p_shannon.append(Node(sym, prob_list[i]))
        p_huffman.append(Node(sym, prob_list[i]))

    # остальной код main без изменений
    shannon_tree = shannon(0, n - 1, p_shannon)
    display_shannon_code(p_shannon, shannon_tree)

    display_in_text_box(text_box, n, symbols, prob_list, p_shannon, p_huffman)


def display_shannon_code(p_list, tree):
    # ваша функция отображения кодов для метода Шеннона-Фано
    pass


def create_interface():
    root = tk.Tk()
    root.title("Расчет вероятностей")

    label1 = tk.Label(root, text="Введите количество символов:")
    label1.pack()

    entry1 = tk.Entry(root)
    entry1.pack()

    label2 = tk.Label(root, text="Введите символы через запятую:")
    label2.pack()

    entry2 = tk.Entry(root)
    entry2.pack()

    label3 = tk.Label(root, text="Введите вероятности или количество выпадений через запятую:")
    label3.pack()

    entry3 = tk.Entry(root)
    entry3.pack()

    text_box = tk.Text(root, height=20, width=50)
    text_box.pack()

    button = tk.Button(root, text="Рассчитать", command=lambda: calculate_probabilities(entry1.get(), entry2.get(),
                                                                                         entry3.get(), text_box))
    button.pack()

    root.mainloop()


def calculate_probabilities(num_symbols, symbol_list, prob_list, text_box):
    n = int(num_symbols)
    symbols = symbol_list.split(",")
    prob_list = [float(x) for x in prob_list.split(",")]

    main(n, symbols, 1, prob_list, text_box)


if __name__ == "__main__":
    create_interface()