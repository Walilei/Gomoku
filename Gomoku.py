import tkinter as tk
import tkinter.messagebox


class Chess:
    radius = 7

    def __init__(self, color):
        self.color = color


class CheckerBoard:
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, height=400, cursor='dot')
        self.checkerboard = tk.PhotoImage(file="2.png")
        self.canvas.create_image(5, 5, anchor='nw', image=self.checkerboard)
        self.canvas.grid(row=0, columnspan=5)
        self.black = Chess('black')
        self.white = Chess('white')
        self.unit = 22  # 棋盤間隔

    def adjust_pos(self, event):  # 調整滑鼠點擊時的座標
        if 25 < event.x < 350 and 25 < event.y < 350:
            nx = (event.x - 35) // 22
            ny = (event.y - 35) // 22
            event.x = 35 + 22 * nx if (event.x - 35) % 22 < 12 else 35 + 22 * (nx + 1)
            event.y = 35 + 22 * ny if (event.y - 35) % 22 < 12 else 35 + 22 * (ny + 1)
            return event.x, event.y


class GameWindow:
    def __init__(self):
        self.board = CheckerBoard()
        self.game_info = tk.Label(self.board.window, width=15, height=2)
        self.game_info.grid(row=2, column=1)
        self.button01 = tk.Button(self.board.window, width=15, height=2)
        self.button01.grid(row=2, column=0)
        self.button02 = tk.Button(self.board.window, width=15, height=2)
        self.button02.grid(row=2, column=2)


class GomokuGame:
    def __init__(self):
        self.window = GameWindow()
        self.window.button01.configure(text='Restart Game', command=self.reset_button)
        self.window.button02.configure(text='Quit', command=self.quit_game)
        self.window.game_info.configure(text='First Round \nBlack\'s turn',
                                        bg='light yellow', font=('Calibri', 12))
        self.turn = ''
        self.focus_icon = tk.PhotoImage(file='3.png')
        self.window.board.canvas.bind('<Double-1>', self.place_chess)
        self.window.board.canvas.bind('<Button-1>', self.select_move)
        self.count = 0
        self.game_history = {'BLACK': [], 'WHITE': []}
        self.unit = self.window.board.unit

    def quit_game(self):
        usr_ans = tk.messagebox.askyesno(title='Confirmation Window', message='This will close the window, sure?')

        if usr_ans is True:
            quit()

    def reset_button(self):
        usr_ans = tk.messagebox.askyesno(title='Confirmation Window', message='This will restart the game, sure?')

        if usr_ans is True:
            self.reset_game()

    def reset_game(self):
        self.window.game_info.configure(text='First Round \nBlack\'s turn')
        self.game_history = {'BLACK': [], 'WHITE': []}
        self.window.board.canvas.delete('focus_icon')
        self.window.board.canvas.delete('chess')
        self.count = 0

    def select_move(self, event):  # 選擇下棋位置
        if 25 < event.x < 350 and 25 < event.y < 350:
            self.window.board.canvas.delete('focus_icon')
            self.window.board.canvas.create_image(self.window.board.adjust_pos(event)[0],
                                                  self.window.board.adjust_pos(event)[1],
                                                  tags='focus_icon', image=self.focus_icon)

    def place_chess(self, event):  # 下棋
        if 25 < event.x < 350 and 25 < event.y < 350:
            event.x, event.y = self.window.board.adjust_pos(event)

            if (event.x, event.y) not in self.game_history['BLACK'] \
                    and (event.x, event.y) not in self.game_history['WHITE']:
                if self.count % 2 == 0:
                    player_name = 'BLACK'
                    self.turn = 'WHITE'
                else:
                    player_name = 'WHITE'
                    self.turn = 'BLACK'

                self.window.board.canvas.create_oval(event.x - Chess.radius, event.y - Chess.radius,
                                                     event.x + Chess.radius, event.y + Chess.radius, fill=player_name,
                                                     tags='chess')
                self.game_history[player_name].append((event.x, event.y))
                self.count += 1
                self.window.game_info.configure(text=f"{self.count} Round(s) \n{self.turn}".title()+'\'s turn')
                self.check_status(event, player_name)

    def end_game(self, player_name):
        tk.messagebox.showinfo(title='CONGRATULATION !!', message=f'{player_name}'.title() +
                                                                  ' player wins!!\n''Press enter for a new game')
        self.reset_game()

    def check_status(self, event, player_name):
        temp = [(event.x, event.y)]
        (x, y) = (event.x, event.y)
        while (x + self.unit, y) in self.game_history[player_name]:
            temp.append((x + self.unit, y))
            x = x + self.unit
        while (x - self.unit, y) in self.game_history[player_name]:
            temp.append((x - self.unit, y))
            x = x - self.unit
        if len(set(temp)) > 4:
            self.end_game(player_name)
        else:
            temp = [(event.x, event.y)]
            (x, y) = (event.x, event.y)
            while (x, y + self.unit) in self.game_history[player_name]:
                temp.append((x, y + self.unit))
                y = y + self.unit
            while (x, y - self.unit) in self.game_history[player_name]:
                temp.append((x, y - self.unit))
                y = y - self.unit
            if len(set(temp)) > 4:
                self.end_game(player_name)
            else:
                temp = [(event.x, event.y)]
                (x, y) = (event.x, event.y)
                while (x + self.unit, y + self.unit) in self.game_history[player_name]:
                    temp.append((x + self.unit, y + self.unit))
                    x, y = x + self.unit, y + self.unit
                while (x - self.unit, y - self.unit) in self.game_history[player_name]:
                    temp.append((x - self.unit, y - self.unit))
                    x, y = x - self.unit, y - self.unit
                if len(set(temp)) > 4:
                    self.end_game(player_name)
                else:
                    temp = [(event.x, event.y)]
                    (x, y) = (event.x, event.y)
                    while (x + self.unit, y - self.unit) in self.game_history[player_name]:
                        temp.append((x + self.unit, y - self.unit))
                        x, y = x + self.unit, y - self.unit
                    while (x - self.unit, y + self.unit) in self.game_history[player_name]:
                        temp.append((x - self.unit, y + self.unit))
                        x, y = x - self.unit, y + self.unit
                    if len(set(temp)) > 4:
                        self.end_game(player_name)


if __name__ == '__main__':
    new_game = GomokuGame()
    new_game.window.board.window.mainloop()

