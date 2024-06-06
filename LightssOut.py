import tkinter as tk
from tkinter import scrolledtext
import random
import time
from collections import deque

class LightsOutGame:
    def __init__(self, root):
        # Inisialisasi jendela Tkinter
        self.root = root
        self.root.title("Lights Out Game")
        # Ukuran grid permainan
        self.size = 3
        # Matriks untuk menyimpan tombol-tombol
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        # Daftar untuk menyimpan langkah-langkah yang diambil pemain
        self.steps = []

        # Membuat tombol-tombol dalam grid
        for row in range(self.size):
            for col in range(self.size):
                # Menggunakan lambda untuk memasukkan argumen ke dalam fungsi toggle_lights
                button = tk.Button(self.root, width=10, height=5, command=lambda r=row, c=col: self.toggle_lights(r, c))
                button.grid(row=row, column=col, padx=0, pady=0)
                self.buttons[row][col] = button

        # Membuat area untuk menampilkan langkah-langkah
        self.steps_display = scrolledtext.ScrolledText(self.root, width=40, height=10)
        self.steps_display.grid(row=self.size, column=0, columnspan=self.size)

        # Tombol untuk memecahkan permainan dengan brute force
        solve_button = tk.Button(self.root, text="Solve (Brute Force)", command=self.solve_and_display_brute_force)
        solve_button.grid(row=self.size + 1, column=0, columnspan=self.size)

        # Tombol untuk memecahkan permainan dengan backtracking
        solve_button = tk.Button(self.root, text="Solve (Backtracking)", command=self.solve_and_display_backtrack)
        solve_button.grid(row=self.size + 2, column=0, columnspan=self.size)

        # Mengacak grid awal
        self.randomize_grid()
        # Menampilkan langkah-langkah awal
        self.update_steps_display()

    def toggle_lights(self, row, col):
        # Menambah langkah ke daftar langkah-langkah
        self.steps.append((row, col))
        self.update_steps_display()

        # Memanggil metode toggle_button untuk mengubah status tombol yang dipilih dan tetangganya
        self.toggle_button(row, col)
        if row > 0:
            self.toggle_button(row-1, col)
        if row < self.size - 1:
            self.toggle_button(row+1, col)
        if col > 0:
            self.toggle_button(row, col-1)
        if col < self.size - 1:
            self.toggle_button(row, col+1)
        
        # Memeriksa apakah pemain menang setelah setiap langkah
        if self.check_win():
            self.show_win_message()
            return True

        return False

    def toggle_button(self, row, col):
        # Mengubah warna latar belakang tombol yang dipilih antara kuning dan default
        button = self.buttons[row][col]
        if button["bg"] == "SystemButtonFace":
            button.config(bg="yellow")
        else:
            button.config(bg="SystemButtonFace")

    def check_win(self):
        # Memeriksa apakah semua lampu sudah dimatikan (warna default)
        for row in range(self.size):
            for col in range(self.size):
                if self.buttons[row][col]["bg"] == "yellow":
                    return False
        return True

    def show_win_message(self):
        # Menampilkan pesan "You Win!" saat pemain menang
        win_message = tk.Label(self.root, text="You Win!", font=("Arial", 24))
        win_message.grid(row=self.size + 3, column=0, columnspan=self.size)

    def update_steps_display(self):
        # Memperbarui area tampilan dengan langkah-langkah terbaru yang diambil oleh pemain
        steps_text = "Steps taken:\n" + "\n".join([f"Step {i+1}: Button ({r},{c})" for i, (r, c) in enumerate(self.steps)])
        self.steps_display.delete("1.0", tk.END)  # Hapus teks yang ada
        self.steps_display.insert(tk.END, steps_text)  # Masukkan teks langkah-langkah baru

    def randomize_grid(self):
        # Mengacak grid awal dengan mengubah warna sejumlah tombol secara acak
        for _ in range(random.randint(5, 15)):
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            self.toggle_button(row, col)

    def solve_brute_force(self):
        # Mencoba semua kemungkinan langkah dengan menggunakan pendekatan brute force
        initial_state = [[button["bg"] for button in row] for row in self.buttons]
        initial_steps = []
        queue = deque([(initial_state, initial_steps)])  # Antrian untuk menyimpan keadaan dan langkah-langkah yang diambil
        visited = set()  # Set untuk menyimpan keadaan yang sudah dikunjungi

        if self.check_win_state(initial_state):
            return initial_steps

        while queue:
            current_state, current_steps = queue.popleft()  # Mengambil keadaan dan langkah-langkah saat ini dari antrian
            current_state_tuple = tuple(tuple(row) for row in current_state)

            if current_state_tuple not in visited:
                visited.add(current_state_tuple)

                if self.check_win_state(current_state):
                    return current_steps

                # Memeriksa setiap tombol dalam keadaan saat ini dan mencoba semua kemungkinan langkah
                for row in range(self.size):
                    for col in range(self.size):
                        new_state = self.toggle_lights_state(current_state, row, col)
                        new_steps = current_steps + [(row, col)]
                        queue.append((new_state, new_steps))

        return None

    def toggle_lights_state(self, state, row, col):
        # Mengubah keadaan tombol dalam matriks state
        new_state = [row[:] for row in state]
        self.toggle_button_state(new_state, row, col)
        if row > 0:
            self.toggle_button_state(new_state, row-1, col)
        if row < self.size - 1:
            self.toggle_button_state(new_state, row+1, col)
        if col > 0:
            self.toggle_button_state(new_state, row, col-1)
        if col < self.size - 1:
            self.toggle_button_state(new_state, row, col+1)
        return new_state

    def toggle_button_state(self, state, row, col):
        # Mengubah keadaan tombol dalam matriks state antara kuning dan default
        if state[row][col] == "SystemButtonFace":
            state[row][col] = "yellow"
        else:
            state[row][col] = "SystemButtonFace"

    def check_win_state(self, state):
        # Memeriksa apakah semua tombol dalam keadaan sudah dimatikan
        for row in range(self.size):
            for col in range(self.size):
                if state[row][col] == "yellow":
                    return False
        return True

    def solve_and_display_brute_force(self):
        # Memecahkan permainan dengan brute force dan menampilkan langkah-langkah solusi serta waktu eksekusi
        start_time = time.time()
        solution = self.solve_brute_force()
        end_time = time.time()

        if solution:
            steps_text = "\n".join([f"Step {i+1}: Button ({r},{c})" for i, (r, c) in enumerate(solution)])
            self.steps_display.insert(tk.END, "\n\nSolved steps (Brute Force):\n" + steps_text)
        else:
            self.steps_display.insert(tk.END, "\n\nNo solution found.")

        execution_time = end_time - start_time
        self.steps_display.insert(tk.END, f"\n\nExecution Time (Brute Force): {execution_time:.7f} seconds")

    def solve_backtrack(self, max_depth=5):
        # Mencoba memecahkan permainan dengan pendekatan backtracking dengan batasan kedalaman pencarian
        initial_state = [[button["bg"] for button in row] for row in self.buttons]
        initial_steps = []
        visited_states = set()  # Set untuk menyimpan keadaan yang sudah dikunjungi
        solution = self.backtrack(initial_state, initial_steps, max_depth, visited_states)
        return solution

    def backtrack(self, state, steps, max_depth, visited_states):
        stack = [(state, steps, max_depth)]  # Stack untuk menyimpan keadaan, langkah, dan kedalaman saat ini

        while stack:
            current_state, current_steps, current_depth = stack.pop()  # Mengambil elemen dari stack

            if self.check_win_state(current_state):
                return current_steps

            if current_depth == 0:
                continue

            # Mengonversi keadaan ke tupel hashable
            state_tuple = tuple(tuple(row) for row in current_state)

            # Memeriksa apakah keadaan saat ini sudah dikunjungi sebelumnya
            if state_tuple in visited_states:
                continue

            visited_states.add(state_tuple)  # Menambah keadaan saat ini ke set keadaan yang sudah dikunjungi

            for row in range(self.size):
                for col in range(self.size):
                    new_state = self.toggle_lights_state(current_state, row, col)
                    new_steps = current_steps + [(row, col)]
                    stack.append((new_state, new_steps, current_depth - 1))  # Menambah elemen baru ke stack

        return None

    def solve_and_display_backtrack(self):
        # Memecahkan permainan dengan pendekatan backtracking dan menampilkan langkah-langkah solusi serta waktu eksekusi
        start_depth = 5  # Kedalaman pencarian awal
        max_depth = start_depth  # Menyimpan nilai kedalaman awal

        self.steps_display.insert(tk.END, f"\n\nAttempting with Max Depth: {max_depth}\n")  # Memasukkan kedalaman maksimal saat ini

        while True:
            start_time = time.time()
            solution = self.solve_backtrack(max_depth)
            end_time = time.time()

            if solution:
                steps_text = "\n".join([f"Step {i+1}: Button ({r},{c})" for i, (r, c) in enumerate(solution)])
                self.steps_display.insert(tk.END, "\nSolved steps (Backtracking):\n" + steps_text)
                break  # Keluar dari loop jika ditemukan solusi
            else:
                max_depth += 5  # Menambah kedalaman pencarian sebesar 5
                self.steps_display.insert(tk.END, f"\nMax depth increased to: {max_depth}\n")  # Memasukkan kedalaman maksimal saat ini

        execution_time = end_time - start_time
        self.steps_display.insert(tk.END, f"\n\nExecution Time (Backtracking): {execution_time:.7f} seconds")

# Membuat jendela utama
root = tk.Tk()

# Inisialisasi permainan
game = LightsOutGame(root)

# Memulai loop peristiwa Tkinter
root.mainloop()
