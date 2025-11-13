import tkinter as tk
import random

class MineSweeper:
    def __init__(self, master, rows=10, cols=10, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = []
        self.mines_loc = set()
        self.flags = set()
        self.opened = set()
        self.game_over = False

        self.frame = tk.Frame(master)
        self.frame.pack()
        self.info = tk.Label(master, text="지뢰찾기 | 좌클릭: 열기 | 우클릭: 깃발")
        self.info.pack()
        self.reset_button = tk.Button(master, text="재시작", command=self.reset_game)
        self.reset_button.pack()
        self.difficulty = tk.Frame(master)
        self.difficulty.pack()
        tk.Button(self.difficulty, text="초급", command=lambda:self.set_difficulty(9,9,10)).pack(side=tk.LEFT)
        tk.Button(self.difficulty, text="중급", command=lambda:self.set_difficulty(16,16,40)).pack(side=tk.LEFT)
        tk.Button(self.difficulty, text="고급", command=lambda:self.set_difficulty(16,30,99)).pack(side=tk.LEFT)
        self.draw_board()

    def set_difficulty(self, r, c, m):
        self.rows = r
        self.cols = c
        self.mines = m
        self.reset_game()

    def draw_board(self):
        # Clear previous buttons
        for row in self.buttons:
            for btn in row:
                btn.destroy()
        self.buttons = []
        for i in range(self.rows):
            line = []
            for j in range(self.cols):
                btn = tk.Button(self.frame, width=2, height=1)
                btn.grid(row=i, column=j)
                btn.bind("<Button-1>", lambda e, x=i, y=j: self.left_click(x, y))
                btn.bind("<Button-3>", lambda e, x=i, y=j: self.right_click(x, y))
                line.append(btn)
            self.buttons.append(line)
        self.place_mines()

    def reset_game(self):
        self.mines_loc = set()
        self.flags = set()
        self.opened = set()
        self.game_over = False
        self.info['text'] = "지뢰찾기 | 좌클릭: 열기 | 우클릭: 깃발"
        self.draw_board()

    def place_mines(self):
        self.mines_loc = set()
        while len(self.mines_loc) < self.mines:
            i = random.randint(0, self.rows-1)
            j = random.randint(0, self.cols-1)
            self.mines_loc.add((i,j))

    def left_click(self, x, y):
        if self.game_over or (x, y) in self.flags: return
        if (x, y) in self.mines_loc:
            self.buttons[x][y].config(text="💣", bg="red")
            self.info['text'] = "게임 오버!"
            self.reveal_mines()
            self.game_over = True
            return
        self.open_cell(x, y)
        if self.check_win():
            self.info['text'] = "성공! 🎉"
            self.game_over = True

    def right_click(self, x, y):
        if self.game_over or (x, y) in self.opened: return
        if (x, y) in self.flags:
            self.buttons[x][y].config(text="")
            self.flags.remove((x,y))
        else:
            self.buttons[x][y].config(text="🚩", fg="blue")
            self.flags.add((x,y))
        if self.check_win():
            self.info['text'] = "성공! 🎉"
            self.game_over = True

    def open_cell(self, x, y):
        if (x, y) in self.opened or (x, y) in self.flags: return
        cnt = sum((nx, ny) in self.mines_loc for nx, ny in self.neighbors(x, y))
        self.buttons[x][y].config(text=str(cnt) if cnt > 0 else "", bg="lightgray", relief=tk.SUNKEN)
        self.opened.add((x, y))
        if cnt == 0:
            for nx, ny in self.neighbors(x, y):
                if 0 <= nx < self.rows and 0 <= ny < self.cols:
                    self.open_cell(nx, ny)

    def neighbors(self, x, y):
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx==0 and dy==0: continue
                yield (x+dx, y+dy)

    def reveal_mines(self):
        for mx, my in self.mines_loc:
            self.buttons[mx][my].config(text="💣", bg="pink")

    def check_win(self):
        return len(self.opened) == self.rows * self.cols - self.mines

if __name__ == "__main__":
    root = tk.Tk()
    root.title("지뢰찾기(Minesweeper) | Python")
    game = MineSweeper(root)
    root.mainloop()
