from tkinter import Tk, Canvas, Label, Frame, simpledialog


class PuzzleCanvas(Canvas):

    def __init__(self, master=None, answers=None, cnf={}, **kw):
        self.width = 605
        self.height = 605
        kwargs = {
            "width": self.width,
            "height": self.height,
            "borderwidth": 0,
            "highlightthickness": 0,
            "relief": "solid",
            "bg": "#000000"
        }
        super().__init__(master, cnf, **kwargs)
        self.place(width=self.width, height=self.height, x=1024 - self.width - 50, y=50)
        self.config(highlightbackground="grey", highlightcolor="grey")
        self.tiles = []

        self.delete('all')
        w, h = 50, 50
        px, py = 2, 2
        num_count = 1
        for y, row in enumerate(answers):
            prev_x_char = ''
            for x, char in enumerate(row):
                next_x_char = row[x + 1] if x < len(row) - 1 else ''
                next_x2_char = row[x + 2] if x < len(row) - 2 else ''
                prev_y_char = answers[y - 1][x] if y > 0 else ''
                next_y_char = answers[y + 1][x] if y < len(answers) - 1 else ''
                x1 = (x * w) + px
                y1 = (y * h) + py
                if char == '_':
                    self.tiles.append(
                        self.create_rectangle(x1, y1, x1 + w, y1 + h, fill='black', outline='black', tags='')
                    )
                else:
                    self.tiles.append(
                        self.create_rectangle(x1, y1, x1 + w, y1 + h, fill='white', outline='black', tags='active')
                    )
                    # is start of column or previous char is inactive then write num
                    if (x == 0 and next_x_char != '_' and next_x2_char != '_') or (prev_x_char == '_' and x < len(row)-1 and next_x_char != '_'):
                        # if this is a new across word then start number label
                        Label(self, text=f"{num_count}.", font='Arial 8 bold', bg='white').place(x=x1+1, y=y1+1)
                        num_count = num_count + 1
                    elif (y == 0 and next_y_char != '_') or (prev_y_char == '_' and y < len(answers)-1 and next_y_char != '_'):
                        # if this is a new down word then start number label
                        Label(self, text=f"{num_count}.", font='Arial 8 bold', bg='white').place(x=x1 + 1, y=y1 + 1)
                        num_count = num_count + 1
                self.tag_bind(self.tiles[-1], '<Enter>', lambda event, obj=self.tiles[-1]: self.mouse_enter(event, obj))
                self.tag_bind(self.tiles[-1], '<Leave>', lambda event, obj=self.tiles[-1]: self.mouse_exit(event, obj))
                self.tag_bind(self.tiles[-1], '<Button-1>', lambda event, obj=self.tiles[-1]: self.mouse_click(event, obj))
                prev_x_char = char

    def mouse_enter(self, event, obj):
        if 'active' in self.gettags("current"):
            self.itemconfig(obj, fill="grey")

    def mouse_exit(self, event, obj):
        if 'active' in self.gettags("current"):
            self.itemconfig(obj, fill="white")

    def mouse_click(self, event, obj):
        if 'active' in self.gettags("current"):
            #print("Click by caller", event, obj)
            input = simpledialog.askstring(title="Answer", prompt="What's your Answer?:")
            print(input)

class CluesCanvas(Canvas):

    def __init__(self, master=None, across_clues=None, down_clues=None, cnf={}, **kwargs):
        super().__init__(master, cnf, **kwargs)
        self.across_clues = across_clues
        self.down_clues = down_clues
        self.frame = Frame()
        self.frame.place(x=20, y=50)
        Label(self.frame, text="Across", font='Arial 16 bold').grid(row=0, column=0, sticky="nw")
        Label(self.frame, text="Down", font='Arial 16 bold').grid(row=0, column=1, sticky="nw")
        num = 0
        for row, clue in enumerate(zip(self.across_clues, self.down_clues), start=1):
            across_clue, down_clue = clue
            num += 1
            Label(self.frame, text=f'{num}.{across_clue}', font='Arial 10', wraplength=170, justify='left').grid(row=row, column=0, sticky="nw", ipady=5)
            num += 1
            Label(self.frame, text=f'{num}.{down_clue}', font='Arial 10', wraplength=170, justify='left').grid(row=row, column=1, sticky="nw", ipady=5)


class CrosswordApp(Tk):

    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):

        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.minsize(1024, 718)
        self.maxsize(1024, 718)
        self.resizable(False, False)
        self.answers = [
            "_FROST_WINDS",
            "H____E_E____",
            "E_CLIMATIC_H",
            "AS_A_P___L_U",
            "THUNDERSTORM",
            "_O_D_R_U_U_I",
            "_W__RAINED_D",
            "PELT_T_____I",
            "OR__GUST_HOT",
            "US_F_R_H_A_Y",
            "R_FORECAST__",
            "___G___W_SKY",
        ]
        self.across_clues = [
            "A white covering on the ground, which is not snow",
            "They blow",
            "El Niño affects ____________ conditions over a large part of the world.",
            "A violent and noisy meteorological event",
            "It ________ so heavily that the road was flooded",
            "To rain very hard.",
            "Sudden short burst of wind.",
            "In summer most people prefer this kind of weather.",
            "A prediction of the weather for the coming day or days.",
            "The rain falls out of it."
        ]
        self.down_clues = [
            "A measurement of heat.",
            "More than just humid.",
            "More than just warmth.",
            "It gets hotter faster than the sea does.",
            "A visible mass of water vapour in the sky.",
            "(A measure of) dampness..",
            "Short periods of rain",
            "It provides us with light in the daytime.",
            "To rain very hard (but not the same as 13 across)",
            "The melting of snow.",
            "People wear them when no.11 is too strong",
            "You cannot see very far through this",
        ]
        self.puzzle = PuzzleCanvas(self, self.answers)
        self.clues = CluesCanvas(self, self.across_clues, self.down_clues)
        self.title("Crossword")
        self.draw()

    def draw(self):
        self.after(16, self.draw)


if __name__ == '__main__':
    app = CrosswordApp()
    app.mainloop()