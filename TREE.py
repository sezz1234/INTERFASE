import tkinter as tk
from tkinter import messagebox

class TreeNode:
    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, root, key):
        if root is None:
            return TreeNode(key)
        if key < root.val:
            root.left = self._insert(root.left, key)
        else:
            root.right = self._insert(root.right, key)
        return root

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, root, key):
        if root is None or root.val == key:
            return root
        if key < root.val:
            return self._search(root.left, key)
        return self._search(root.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, root, key):
        if root is None:
            return root
        if key < root.val:
            root.left = self._delete(root.left, key)
        elif key > root.val:
            root.right = self._delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            root.val = self._min_value_node(root.right)
            root.right = self._delete(root.right, root.val)
        return root

    def _min_value_node(self, node):
        while node.left is not None:
            node = node.left
        return node.val

    def bfs(self):
        result = []
        if self.root is not None:
            queue = [self.root]
            while queue:
                node = queue.pop(0)
                result.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
        return result

    def inorder(self):
        return self._inorder(self.root, [])

    def _inorder(self, root, result):
        if root:
            result = self._inorder(root.left, result)
            result.append(root.val)
            result = self._inorder(root.right, result)
        return result

class BSTApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Графический интерфейс для Бинарного Дерева Поиска")
        self.create_gui()

    def create_gui(self):
        # Frame to hold the input fields and buttons
        input_frame = tk.Frame(self.master)
        input_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Entry and Button for inserting a node
        self.insert_entry = tk.Entry(input_frame)
        self.insert_entry.pack(side=tk.TOP, padx=5, pady=5)
        insert_button = tk.Button(input_frame, text="Вставить", command=self.insert_node)
        insert_button.pack(side=tk.TOP, padx=5, pady=5)

        # Entry and Button for searching a node
        self.search_entry = tk.Entry(input_frame)
        self.search_entry.pack(side=tk.TOP, padx=5, pady=5)
        search_button = tk.Button(input_frame, text="Поиск", command=self.search_node)
        search_button.pack(side=tk.TOP, padx=5, pady=5)

        # Entry and Button for deleting a node
        self.delete_entry = tk.Entry(input_frame)
        self.delete_entry.pack(side=tk.TOP, padx=5, pady=5)
        delete_button = tk.Button(input_frame, text="Удалить", command=self.delete_node)
        delete_button.pack(side=tk.TOP, padx=5, pady=5)

        # Frame to hold the traversal results
        result_frame = tk.Frame(self.master)
        result_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Button for displaying BFS traversal
        bfs_button = tk.Button(result_frame, text="BFS Обход", command=self.display_bfs)
        bfs_button.pack(side=tk.TOP, padx=5, pady=5)

        # Button for displaying Inorder traversal
        inorder_button = tk.Button(result_frame, text="DFS Обход", command=self.display_inorder)
        inorder_button.pack(side=tk.TOP, padx=5, pady=5)

        # Label to display traversal results
        self.result_label = tk.Label(result_frame, text="")
        self.result_label.pack(side=tk.TOP, padx=5, pady=5)

    def insert_node(self):
        try:
            key = int(self.insert_entry.get())
            bst.insert(key)
            messagebox.showinfo("Успех", f"Узел {key} успешно вставлен!")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите целое число.")

    def search_node(self):
        try:
            key = int(self.search_entry.get())
            node = bst.search(key)
            if node:
                messagebox.showinfo("Успех", f"Узел {key} найден в дереве!")
            else:
                messagebox.showinfo("Не найдено", f"Узел {key} не найден в дереве.")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите целое число.")

    def delete_node(self):
        try:
            key = int(self.delete_entry.get())
            bst.delete(key)
            messagebox.showinfo("Успех", f"Узел {key} успешно удален!")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите целое число.")

    def display_bfs(self):
        bfs_result = bst.bfs()
        self.result_label.config(text=f"BFS Обход: {bfs_result}")

    def display_inorder(self):
        inorder_result = bst.inorder()
        self.result_label.config(text=f"DFS Обход: {inorder_result}")

if __name__ == "__main__":
    root = tk.Tk()
    bst = BinarySearchTree()
    app = BSTApp(root)
    root.mainloop()