from tkinter import Tk, Canvas, Label, Frame, simpledialog, LEFT, RIGHT, BOTH, Y, X

class Puzzle:

    def __init__(self, master=None, answers=None, across_clues=None, down_clues=None):
        self.tiles = []

        # setup frames for left and right
        self.clue_frame = Frame(master, bd=0, relief='solid')
        self.clue_frame.pack(side=LEFT, fill=Y, padx=20, pady=50)
        self.puzzle_frame = Frame(master, bd=0, relief='solid')
        self.puzzle_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=0, pady=50)

        # add clue label titles for down and across
        Label(self.clue_frame, text="Across", font='Arial 16 bold').grid(row=0, column=0, sticky="nw")
        Label(self.clue_frame, text="Down", font='Arial 16 bold').grid(row=0, column=1, sticky="nw")

        # setup canvas for drawing the puzzle on right side
        self.puzzle_canvas = Canvas(self.puzzle_frame, bg="#000000", relief="solid", borderwidth=0, highlightthickness=0)
        self.puzzle_canvas.place(width=605, height=605)

        # setup square dimensions and padding
        square_w, square_h = 50, 50
        square_px, square_py = 2, 2

        num_count = 1
        across_clue_index, down_clue_index = 0, 0

        self.puzzle_canvas.bind_all('<Key>', self.key_press)

        for y, row in enumerate(answers):
            for x, current_char in enumerate(row):
                # lets assign some understandable variables for checking
                start_word = False
                prev_char = row[x - 1] if x > 0 else ''
                next_char = row[x + 1] if x < len(row) - 1 else ''
                next_char2 = row[x + 2] if x < len(row) - 2 else ''
                prev_char_above = answers[y - 1][x] if y > 0 else ''
                next_char_below = answers[y + 1][x] if y < len(answers) - 1 else ''
                is_first_char = x == 0
                is_next_2_chars_valid = next_char != '_' and next_char2 != '_'
                is_first_row = y == 0

                # setup rect sizes
                x1 = (x * square_w) + square_px
                y1 = (y * square_h) + square_py

                if current_char != '_':
                    rect_kwargs = {'fill': 'white', 'tags': f'rect_{x}_{y} word'}
                    #  (Across)
                    #  if we are on the leftmost character, and it's a word (3 or more) OR
                    #  we are starting a new word on the row, and it's not the end
                    if (is_first_char and is_next_2_chars_valid) or (prev_char == '_' and next_char not in ('_', '')):
                        self.puzzle_canvas.create_text(x1 + 1 + 10, y1 + 1 + 10, text=f"{num_count}.", fill="black", font='Arial 8 bold')
                        Label(self.clue_frame, text=f'{num_count}. {across_clues[across_clue_index]}', font='Arial 10',
                              wraplength=170, justify='left').grid(row=across_clue_index + 1, column=0, sticky="nw",
                                                                   ipady=5)
                        across_clue_index = across_clue_index + 1
                        start_word = True

                    # (Down)
                    # if we are the topmost character, and it's a word OR
                    # We are starting a new word on the column, and it's not the end
                    if (is_first_row and next_char_below != '_') or (prev_char_above == '_' and next_char_below not in ('_', '')):
                        self.puzzle_canvas.create_text(x1 + 1 + 10, y1 + 1 + 10, text=f"{num_count}.", fill="black", font='Arial 8 bold')
                        Label(self.clue_frame, text=f'{num_count}. {down_clues[down_clue_index]}', font='Arial 10',
                              wraplength=170, justify='left').grid(row=down_clue_index + 1, column=1, sticky="nw",
                                                                   ipady=5)
                        down_clue_index = down_clue_index + 1
                        start_word = True

                    if start_word:
                        num_count += 1
                else:
                    rect_kwargs = {'fill': 'black', 'tags': f'rect_{x}_{y}'}

                # let's create each rectangle black/white and assign event handlers and lower below numbers
                rect = self.puzzle_canvas.create_rectangle(x1, y1, x1 + square_w, y1 + square_h, **rect_kwargs)
                self.puzzle_canvas.tag_lower(rect)
                if 'word' in rect_kwargs['tags']:
                    self.puzzle_canvas.tag_bind(rect, '<Enter>', lambda event, obj=rect: self.mouse_enter(event, obj))
                    self.puzzle_canvas.tag_bind(rect, '<Leave>', lambda event, obj=rect: self.mouse_exit(event, obj))
                    self.puzzle_canvas.tag_bind(rect, '<Button-1>', lambda event, obj=rect: self.mouse_click(event, obj))

    def mouse_enter(self, event, obj):
        """
        Set square grey on mouse enter
        :param event: event object
        :param obj: object on canvas
        """
        if 'active' not in self.puzzle_canvas.gettags("current"):
            self.puzzle_canvas.itemconfig(obj, fill="grey")

    def mouse_exit(self, event, obj):
        """
        Set square white on mouse exit
        :param event: event object
        :param obj: object on canvas
        """
        if 'active' not in self.puzzle_canvas.gettags("current"):
            self.puzzle_canvas.itemconfig(obj, fill="white")

    def mouse_click(self, event, obj):
        """
        Take user input on mouse clicking a square
        :param event: event object
        :param obj: object on canvas
        """
        self.clear_active()
        self.set_active(obj)

    def key_press(self, event):
        # find active one and set the Character to event.char.
        for item in self.puzzle_canvas.find_withtag('active'):
            coords = self.puzzle_canvas.coords(item)
            # clear old char
            for char_item in self.puzzle_canvas.find_withtag(f'char_{coords[0]}_{coords[1]}'):
                self.puzzle_canvas.delete(char_item)
            # add new char
            self.puzzle_canvas.create_text(coords[0] + 25, coords[1] + 25, text=event.char.upper(), fill="black", font='Arial 14 bold', tags=f'char_{coords[0]}_{coords[1]}')
            self.increment_active(item)
        self.check_win_conditions()

    def clear_active(self):
        # clear existing active tags
        for item in self.puzzle_canvas.find_withtag('active'):
            item_tags = self.puzzle_canvas.gettags(item)
            clean_tags = list(filter(lambda x: (x != 'active'), item_tags))
            self.puzzle_canvas.itemconfig(item, tags=clean_tags)
            self.puzzle_canvas.itemconfig(item, fill="white")

    def set_active(self, obj):
        # add active tag and set color
        tags = self.puzzle_canvas.gettags(obj)
        tags += ('active',)
        self.puzzle_canvas.itemconfig(obj, tags=tags)
        self.puzzle_canvas.itemconfig(obj, fill="#ADD8E6")

    def increment_active(self, item):
        rect_tag = ''
        item_tags = self.puzzle_canvas.gettags(item)
        rect_tags = list(filter(lambda x: x.startswith('rect_'), item_tags))
        rect_tag = rect_tags[0] if rect_tags else ''
        self.clear_active()
        if rect_tag:
            _, x, y = rect_tag.split('_')
            next = self.puzzle_canvas.find_withtag(f'rect_{int(x) + 1}_{y}')
            if "word" not in self.puzzle_canvas.gettags(next):
                next = None
            if next:
                self.set_active(next)


class CrosswordApp(Tk):

    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        """
        Thank you to linguapress for permission to use their crossword puzzle and clues which can be found here
        https://linguapress.com/puzzles/weather-crossword.htm
        """
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
        self.puzzle = Puzzle(self, self.answers, self.across_clues, self.down_clues)
        self.title("Crossword")
        self.draw()

    def draw(self):
        self.after(16, self.draw)


if __name__ == '__main__':
    app = CrosswordApp()
    app.mainloop()