import numpy as np
import tkinter as tk
from tkinter import ttk

def filling_list(ribs, entries):
    RibsList = [0] * ribs
    for i in range(ribs):
        a = int(entries[i * 2].get())
        b = int(entries[i * 2 + 1].get())
        RibsList[i] = [a, b]
    return RibsList

def adjacency_matrix(LenghtList, ribs, RibsList):
    min_vertex = min(min(edge) for edge in RibsList)
    max_vertex = max(max(edge) for edge in RibsList)

    adjacency_matrix_list = [[0] * (max_vertex - min_vertex + 1) for _ in range(max_vertex - min_vertex + 1)]

    if flag == 1:
        coefficient = -1
    else:
        coefficient = 1

    for i in range(ribs):
        a = RibsList[i][0] - min_vertex
        b = RibsList[i][1] - min_vertex
        if RibsList[i][0] != RibsList[i][1]:
            adjacency_matrix_list[a][b] = 1
            adjacency_matrix_list[b][a] = 1 * coefficient

    return adjacency_matrix_list

def adjacency_list(adjacency_matrix_list, LenghtList, ribs):
    result_text.insert(tk.END, "\n\nСписок смежности\n")
    for i in range(LenghtList):
        temp_list = [i+1]
        for j in range(LenghtList):
            a = j + 1
            if adjacency_matrix_list[i][j] == 1:
                temp_list.append(a)

        result_text.insert(tk.END, np.array(temp_list))
        temp_list.clear()

def incidence_matrix(LenghtList, ribs, RibsList):
    result_text.insert(tk.END, "\n\nМатрица инцидентности\n")
    incidence_matrix_list = [0] * LenghtList
    for i in range(LenghtList):
        incidence_matrix_list[i] = [0] * ribs

    if flag == 1:
        coefficient = -1
    else:
        coefficient = 1

    for i in range(ribs):
        a = RibsList[i][0]
        b = RibsList[i][1]
        incidence_matrix_list[a-1][i] = 1
        incidence_matrix_list[b-1][i] = 1 * coefficient

    result_text.insert(tk.END, str(np.matrix(incidence_matrix_list)))

def run_program():
    global flag
    flag = int(graph_type.get())
    ribs = int(entry_ribs.get())
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    entries = []
    for i in range(ribs):
        label_edge = tk.Label(root, text="Ребро {}: ".format(i + 1))
        label_edge.grid(row=i + 4, column=0, padx=5, pady=5)
        entry_a = tk.Entry(root)
        entry_a.grid(row=i + 4, column=1, padx=5, pady=5)
        entry_b = tk.Entry(root)
        entry_b.grid(row=i + 4, column=2, padx=5, pady=5)
        entries.extend([entry_a, entry_b])

    run_button.grid_forget()
    execute_button = tk.Button(root, text="Анализ графа", command=lambda: analyze_graph(entries, ribs))
    execute_button.grid(row=ribs + 5, column=1, columnspan=2, pady=10)

def analyze_graph(entries, ribs):
    RibsList = filling_list(ribs, entries)
    LenghtList = len(set(sum(RibsList, [])))
    result_text.insert(tk.END, "Количество вершин: " + str(LenghtList) + "\n")
    adjacency_matrix_list = adjacency_matrix(LenghtList, ribs, RibsList)
    result_text.insert(tk.END, "\nМатрица смежности:\n" + str(np.matrix(adjacency_matrix_list)))
    adjacency_list(adjacency_matrix_list, LenghtList, ribs)
    incidence_matrix(LenghtList, ribs, RibsList)
    result_text.config(state=tk.DISABLED)


root = tk.Tk()
root.title("Graph Program")

label_graph_type = tk.Label(root, text="Выберите тип графа:")
label_graph_type.grid(row=0, column=0, padx=5, pady=5)

graph_type = tk.StringVar()
graph_type.set("1")

radio_button_oriented = tk.Radiobutton(root, text="Ориентированный", variable=graph_type, value="1")
radio_button_oriented.grid(row=1, column=0, padx=5, pady=5)

radio_button_non_oriented = tk.Radiobutton(root, text="Неориентированный", variable=graph_type, value="2")
radio_button_non_oriented.grid(row=2, column=0, padx=5, pady=5)

label_ribs = tk.Label(root, text="Введите количество ребер:")
label_ribs.grid(row=3, column=0, padx=5, pady=5)

entry_ribs = tk.Entry(root)
entry_ribs.grid(row=3, column=1, padx=5, pady=5)

run_button = tk.Button(root, text="Выполнить", command=run_program)
run_button.grid(row=3, column=2, padx=5, pady=5)

result_text = tk.Text(root, height=20, width=60, state=tk.DISABLED)
result_text.grid(row=0, column=3, rowspan=100, padx=10, pady=10)

root.mainloop()