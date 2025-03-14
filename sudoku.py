"""
MCOMP Computer Science - Level 1
CMP1902M Programming Fundamentals: Assessment 2 (Task 2: Sudoku)
Author: John Brock
Student ID: 11216709
Email: 11216709@students.lincoln.ac.uk
Date submitted: 03/02/2022y
"""

import time, random

class Screen:
    """Utility class for moving around and printing nicely to the terminal.

    All methods can be called directly on the class without initialising it 
    via Screen() first.
        e.g. Screen.clear()

    Mainly uses ANSI escape codes to work where the ESCAPE key is simulated and
    followed with commands to interact with the terminal.
    For further info see here: https://en.wikipedia.org/wiki/ANSI_escape_code
    """

    def ansi_compatibility_check():
        """Print a test screen and asks the user to confirm it appears in colour.

        The game display relies heavily on being able to render colour and 
        refresh the screen. If user confirms colours aren't shown, they are 
        given a link to download a compatible CLI (the new Windows Terminal).
        """

        logo = [
            " __          __  _                           ",
            " \ \        / / | |                          ",
            "  \ \  /\  / /__| | ___ ___  _ __ ___   ___  ",
            "   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ ",
            "    \  /\  /  __/ | (_| (_) | | | | | |  __/ ",
            "     \/  \/ \___|_|\___\___/|_| |_| |_|\___| "
        ]

        print(" \u001b[31m╭{}╮\u001b[0m".format("─" * 68))
        print(" \u001b[31m│{}│\u001b[0m".format(" " * 68))
        for line in logo:
            print(" \u001b[31m│\u001b[34m{}\u001b[31m│\u001b[0m".format(line.center(68)))
        print(" \u001b[31m│{}│\u001b[0m".format(" " * 68))  
        print(" \u001b[31m╰{}╯\u001b[0m".format("─" * 68))
        print("")
        print("  Is the text above blue with a red border?")
        while True:
            user_input = input("  Enter (Y)es or (N)o: ").lower().strip()
            if user_input in ["yes", "y"]:
                return
            elif user_input in ["no", "n"]:
                print("")
                print(" ╭{}╮".format("─" * 68))
                print(" │{}│".format(" " * 68))
                print(" │{}│".format(":(".center(68)))
                print(" │{}│".format(" " * 68))
                print(" │{}│".format("Oh no! This terminal doesn't support this game.".center(68)))
                print(" │{}│".format(" " * 68))
                print(" │{}│".format("Please use a Terminal that supports ANSI escape codes and colours.".center(68)))
                print(" │{}│".format(" " * 68))
                print(" │{}│".format("A good terminal to use is the new Windows Terminal.".center(68)))
                print(" │{}│".format("https://www.microsoft.com/en-gb/p/windows-terminal/9n0dx20hk701".center(68)))
                print(" │{}│".format(" " * 68))
                print(" ╰{}╯".format("─" * 68))
                exit()
            else:
                print("  That isn't a valid answer, please try again.")
                continue

    def move_up(lines = 1):
        """Moves the terminal cursor up by a number of lines.

        Prints ANSI escape code CSI {n} A where n is the number of lines.
        Does not output a line-return "\n" character.

        Args:
            lines (int): Number of lines to move the cursor up by (default is 1).
        """

        print("\u001b[{}A".format(lines), end="")

    def move_down(lines = 1):
        """Moves the termainl cursor down by a number of lines.

        Prints ANSI escape code CSI {n} B where n is the number of lines.
        Does not output a line-return "\n" character.

        Args:
            lines (int): Number of lines to move the cursor down by 
                (default is 1).
        """

        print("\u001b[{}B".format(lines), end="")

    def move_right(chars = 1):
        """Moves the termainl cursor right by a number of characters.

        Prints ANSI escape code CSI {n} C where n is the number of characters.
        Does not output a line-return "\n" character.

        Args:
            chars (int): Number of characters to move the cursor right by 
                (default is 1).
        """

        print("\u001b[{}C".format(chars), end="")

    def move_left(chars = 1):
        """Moves the termainl cursor left by a number of characters.

        Prints escape code CSI {n} D where n is the number of characters.
        Does not output a line-return "\n" character.

        Args:
            chars(int): Number of characters to move the cursor left by 
                (default is 1).
        """

        print("\u001b[{}D".format(chars), end="")

    def clear():
        """Wipes the visible screen of content.

        Moves cursor positon to top left corner of screen (CSI escape code H) 
        and then erases all of current display (CSI escape code J).

        See https://en.wikipedia.org/wiki/ANSI_escape_code#CSI_(Control_Sequence_Introducer)_sequences
        """
        
        print("\x1b[H\x1b[J")

    def print_error(*args, **kwargs):
        """Formats and prints error message to the screen.
        
        Returns:
            String of the error message text. Useful for further analysis of what
            was printed to the termainl.
        """
        
        sep = kwargs.get("sep", " ")
        end = kwargs.get("end", "\n")
        text = sep.join(args)
        text = "WHOOPS! {}".format(text)
        text = Screen.wrap_string(text, 66)
        line_count = text.count("\n") + 1
        for i in range(line_count):
            print(" │{}│\u001b[0K".format(" " * 68))

        text = text.replace("\n", "\n\u001b[3C")  # Move to show border.

        Screen.move_up(line_count)
        print(" │ \u001b[31m{}\u001b[0m".format(text), end=end)

        return text + end

    def wrap_string(text, wrap_length, alignment="left"):
        """Wraps the string to a certain length, adding newlines or hyphenating.

        Will try to add new lines at the closest space. If no space is found,
        then will hyphenate the word at the end of the available space.
        
        Args:
            text (str): The text to wrap.
            wrap_length (int): The inclusive length to wrap by.
            alignment (str): Whether to align the text right, center, or left.
                Default is left.

        Returns:
            String of the wrapped text.
        """

        if not alignment in ["left", "center", "right"]:
            raise ValueError("Invalid string alignment specified.")

        if alignment == "left":
            align_function = "ljust"
        elif alignment == "center":
            align_function = "center"
        elif alignment == "right":
            align_function = "rjust"

        if len(text) <= wrap_length:
            return eval("text.{}({})".format(align_function, wrap_length))
        
        wrapped_text = ""

        while text != "":
            for i in range(wrap_length, -1, -1):
                space = text.find(" ", i, wrap_length + 1)
                if space != -1:
                    wrapped_text = wrapped_text + eval("text[0:space].strip().{}({})".format(align_function, wrap_length)) + "\n"
                    text = text[space:].strip()
                elif len(text) <= wrap_length:
                    wrapped_text = wrapped_text + eval("text.strip().{}({})".format(align_function, wrap_length))
                    text = ""
                    break
                elif i == 0:
                    wrapped_text = wrapped_text + eval("text[0:(wrap_length-1)].{}({})".format(align_function, wrap_length)) + "-\n"
                    text = text[(wrap_length-1):].strip()
        
        return wrapped_text

    def red_text(text):
        """Returns the input wrapped in commands to turn the text red.
        
        Args:
            text (str): Text to make red.

        Returns:
            String of text wrapped in ESC[31m and ESC[0m which turns the text
            red when printed to the console. Includes a reset to ensure 
            following text isn't also red.
        """

        return ("\u001b[31m{}\u001b[0m".format(text))
    
    def green_text(text):
        """Returns the input wrapped in commands to turn the text green.
        
        Args:
            text (str): Text to make green.

        Returns:
            String of text wrapped in ESC[32m and ESC[0m which turns the text
            green when printed to the console. Includes a reset to ensure 
            following text isn't also green.
        """

        return ("\u001b[32m{}\u001b[0m".format(text))

    def yellow_text(text):
        """Returns the input wrapped in commands to turn the text yellow.
        
        Args:
            text (str): Text to make yellow.

        Returns:
            String of text wrapped in ESC[33m and ESC[0m which turns the text
            yellow when printed to the console. Includes a reset to ensure 
            following text isn't also yellow.
        """

        return ("\u001b[33m{}\u001b[0m".format(text))

    def blue_text(text):
        """Returns the input wrapped in commands to turn the text blue.
        
        Args:
            text (str): Text to make blue.

        Returns:
            String of text wrapped in ESC[34m and ESC[0m which turns the text
            blue when printed to the console. Includes a reset to ensure 
            following text isn't also blue.
        """

        return ("\u001b[34m{}\u001b[0m".format(text))

    def magenta_text(text):
        """Returns the input wrapped in commands to turn the text magenta.
        
        Args:
            text (str): Text to make magenta.

        Returns:
            String of text wrapped in ESC[35m and ESC[0m which turns the text
            magenta when printed to the console. Includes a reset to ensure 
            following text isn't also magenta.
        """

        return ("\u001b[35m{}\u001b[0m".format(text))

    def human_bool(bool):
        """Converts boolean values into a friendly "Yes" or "No" format.

        Also recognises boolean values expressed as integers or strings
        
        Args:
            bool (bool|int|str): A value that can be recognised as a boolean.

        Returns:
            A string literal of "Yes" or "No".
        """

        if isinstance(bool, str):
            bool = bool.lower()
        if bool not in [True, False, 1, 0, "1", "0", "yes", "no"]:
            raise ValueError("Input value is not recognised as a boolean.")
        return "Yes" if bool in [True, 1, "1", "yes"] else "No"

    def human_duration(time_in_seconds):
        """Converts the give seconds indo a friendly format.
        
        Args:
            time_in_seconds (float): seconds and milliseconds to convert into 
                a friendly representation.
        
        Returns:
            A string representing the duration. 
            
            If the time is less than 60 seconds, it will return 
            "{seconds.milliseconds} seconds". 
            Milliseconds will only be included if there are any.

            If the time is greater than 60 seconds and less than 1 hour, it will
            return "{minutes} minutes and {seconds.milliseconds} seconds".

            If the time is greater than 60 minutes, it will return
            "{hours} hours, {minutes} minutes and {seconds.milliseconds} seconds."
        """
        
        milliseconds = round(time_in_seconds % 1, 2)
        seconds = int(time.strftime("%S", time.gmtime(time_in_seconds)))
        if milliseconds and time_in_seconds < 60:
            seconds = seconds + milliseconds
        ret = "{} seconds".format(str(seconds))

        if time_in_seconds >= 60:
            minutes = int(time.strftime("%M", time.gmtime(time_in_seconds)))
            text = "minutes" if minutes > 1 else "minute"
            ret = "{} {} and {}".format(str(minutes), text, ret)

        if time_in_seconds >= 3600:
            hours = int(time.strftime("%H", time.gmtime(time_in_seconds)))
            text = "hours" if hours > 1 else "hour"
            ret = "{} {}, {}".format(hours, text, ret)
        return ret

class Sudoku:
    """Allows users to play sudoku via a supported CLI.
    
    Coupled heavily with Screen class. To begin, call Sudoku.start() and this
    class takes care of the rest. All settings and game options are printed
    directly to the terminal.

    Language:
        "Board" is used to refer to the full space the game can be played on.
        "Col" or "Column" refers to the vertical parts of the board.
        "Row" refers to the horizontal parts of the board.
        "Grid" refers to the 3x3 squares that hold 9 numbers.
        "Cell" refers to an individual box a number can be entered into.

    Attributes:
        allow_undos (bool): Whether to allow the player to undo previous moves.
        board (list): Current board being played.
        board_choice (int): Which board is currently being played (1-4). 
            Default is 2.
        col_header_colour (str): The colour that the col headers should render.
        colour_options (list): The available colours a user can set for the game.
        game_in_progress (bool): Whether a game is currently being played. 
            Default is False.
        game_input_order (list): The order of questions to ask when playing.
        game_mode (str): An indication who is playing the game: 'player' or 
            'computer'. Default is 'player'.
        game_solvable (bool): Whether the current board is solvable. 
            Default is True.
        game_start (int): The time that the game began (seconds since Epoch).
        game_time (int): The number of seconds it took to complete the game.
        game_timer (int): Used to time the game. When a game is paused, this is 
            used to increase the game_time and is reset when the game is unpaused.
        game_won (bool): Whether the current game has been won. Default is False.
        grid_colour (str): The colour that the grid should render.
        grid_text_colour: The colour of the games starting text.
        move_history (list): List of all moves made by the player so far.
        number_of_moves (int): Number of moves the user has made in the game.
        possible_numbers (list): The possiible numbers for each cell.
        row_header_colour (str): The colour that the row headers should render.
        selection_colour: The colour that that current selection should render. 
            Note: Player moves also highlight this colour.
        show_computer_moves (bool): Whether to show the moves the computer is 
            making while solving the game. Default is False as slows solve time 
            (due to time refreshing the board).
        solved_board (list): Saves the solved board to make giving hints quicker.
        sudoku1 (list[list]): Game 1 of Sudoku, as definied by assignment.
        sudoku2 (list[list]): Game 2 of Sudoku, as definied by assignment.
        sudoku3 (list[list]): Game 3 of Sudoku, as definied by assignment.
        sudoku4 (list[list]): Game 4 of Sudoku, as definied by assignment.
    """

    # Sudoku games - as defined in assignment.
    sudoku1 = [
        [' ', '1', '5', '4', '7', ' ', '2', '6', '9'],
        [' ', '4', '2', '3', '5', '6', '7', ' ', '8'],
        [' ', '8', '6', ' ', ' ', ' ', ' ', '3', ' '],
        ['2', ' ', '3', '7', '8', ' ', ' ', ' ', ' '],
        [' ', ' ', '7', ' ', ' ', ' ', ' ', '9', ' '],
        ['4', ' ', ' ', ' ', '6', '1', ' ', ' ', '2'],
        ['6', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '4', ' ', ' ', ' ', '1', ' ', '7'],
        [' ', ' ', ' ', ' ', '3', '7', '9', '4', ' '],
    ]
    sudoku2 = [
        [' ', ' ', ' ', '3', ' ', ' ', ' ', '7', ' '],
        ['7', '3', '4', ' ', '8', ' ', '1', '6', '2'],
        ['2', ' ', ' ', ' ', ' ', ' ', ' ', '3', '8'],
        ['5', '6', '8', ' ', ' ', '4', ' ', '1', ' '],
        [' ', ' ', '2', '1', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '7', '8', ' ', ' ', '2', '5', '4'],
        [' ', '7', ' ', ' ', ' ', '2', '8', '9', ' '],
        [' ', '5', '1', '4', ' ', ' ', '7', '2', '6'],
        ['9', ' ', '6', ' ', ' ', ' ', ' ', '4', '5'],
    ]
    sudoku3 = [
        ['8', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '3', '6', ' ', ' ', ' ', ' ', ' '],
        [' ', '7', ' ', ' ', '9', ' ', '2', ' ', ' '],
        [' ', '5', ' ', ' ', ' ', '7', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '4', '5', '7', ' ', ' '],
        [' ', ' ', ' ', '1', ' ', ' ', ' ', '3', ' '],
        [' ', ' ', '1', ' ', ' ', ' ', ' ', '6', '8'],
        [' ', ' ', '8', '5', ' ', ' ', ' ', '1', ' '],
        [' ', '9', ' ', ' ', ' ', ' ', '4', ' ', ' '],
    ]
    sudoku4 = [
        [' ', '4', '1', ' ', ' ', '8', ' ', ' ', ' '],
        ['3', ' ', '6', '2', '4', '9', ' ', '8', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' '],
        [' ', ' ', ' ', '4', '7', ' ', '2', '1', ' '],
        ['7', ' ', ' ', '3', ' ', ' ', '4', ' ', '6'],
        [' ', '2', ' ', ' ', ' ', ' ', ' ', '5', '3'],
        [' ', ' ', '7', ' ', '9', ' ', '5', ' ', ' '],
        [' ', ' ', '3', ' ', '2', ' ', ' ', ' ', ' '],
        [' ', '5', '4', ' ', '6', '3', ' ', ' ', ' '],
    ]

    colour_options = [
        "\u001b[31m",
        "\u001b[32m",
        "\u001b[33m",
        "\u001b[34m",
        "\u001b[35m",
        "\u001b[36m",
        "\u001b[37m",
        "\u001b[38;5;88m",
        "\u001b[38;5;202m",
        "\u001b[38;5;22m",
        "\u001b[38;5;19m",
        "\u001b[38;5;162m",
        "\u001b[38;5;24m",
        "\u001b[38;5;240m",
    ]

    def __init__(self):
        """Sets the board and all default instance variables."""

        self.number_of_moves = 0
        self.game_mode = 'player'
        self.show_computer_moves = False
        self.allow_undos = False
        self.game_start = 0
        self.game_time = 0
        self.game_end = 0
        self.game_timer = 0
        self.game_in_progress = False
        self.grid_colour = self.colour_options[6]
        self.row_header_colour = self.colour_options[11]
        self.col_header_colour = self.colour_options[8]
        self.selection_colour = self.colour_options[3]
        self.grid_text_colour = self.colour_options[6]
        self.move_history = []
        self.solved_board = []
        self.game_input_order = ["row", "column", "value"]
    
    def start_timer(self, reset = False):
        """Stores start time in order to track duration of play.
        
        Args:
            reset (bool): Wherther to reset the timer or not. If set to True,
                will reset all metric tracking for game. Default is False.
        """

        if not self.game_start or reset:
            self.game_start = time.time()
            self.game_time = 0
            self.number_of_moves = 0
        self.game_timer = time.time()

    def stop_timer(self):
        """Calculates the time played and stores it.
        
        Raises:
            AttributeError: A timer hasn't been started yet.
        """

        if not self.game_timer:
            raise AttributeError('Timer has not been started.')

        time_elapsed = time.time() - self.game_timer
        self.game_time = self.game_time + time_elapsed
    
    def set_board(self, board):
        """Sets the board to be played, as well as resetting all game metrics.
        
        Args:
            board (int): The board to be played. Valid options are 1, 2, 3 or 4.

        Raises:
            ValueError: An invalid board number has been requested.
        """

        if board not in range(1, 5):
            raise ValueError("Invalid board choice!")

        self.board = []
        self.hint_board = []
        self.possible_numbers = []
        self.hint_possible_numbers = []
        self.board_choice = board        
        self.game_in_progress = False
        self.game_won = False
        self.hint_game_in_progress = False
        self.hint_game_won = False
        self.game_solvable = True
        self.move_history = []
        self.solved_board = []

        for row_id, row in enumerate(eval("self.sudoku{}".format(str(board)))):
            self.board.append([])
            self.hint_board.append([])
            self.possible_numbers.append([])
            self.hint_possible_numbers.append([])

            for value in row:
                self.board[row_id].append(value)
                self.hint_board[row_id].append(value)
                if value.strip() == "":
                    self.possible_numbers[row_id].append([0])
                    self.hint_possible_numbers[row_id].append([0])
                else: 
                    self.possible_numbers[row_id].append([])
                    self.hint_possible_numbers[row_id].append([])

    def update_board(self, row_id, col_id, value, board=[]):
        """Validates the input and updates the board.
        
        Args:
            row_id (int): The row number to be updated (zero-indexed).
            col_id (int): The column number to be updated (zero-indexed).
            value (int): The value to be set.

        Raises:
            ValueError: Trying to set a value to an invalid location, or trying
                to set an invalid value.
        """

        if not board:
            board = self.board

        valid_values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", " "]
        
        if row_id not in range(9) or col_id not in range(9):
            raise ValueError("Trying to set a value in an invalid location.")
        elif str(value) not in valid_values:
            raise ValueError("Trying to add an invalid number to the grid.")

        board[row_id][col_id] = str(value)

    def user_entered(self, row_id, col_id):
        """Compares the location to the original board to detect whether the
        value was a default value, or added by the player
        
        Args:
            row_id (int): The row number to be checked (zero-indexed).
            col_id (int): The column number to be checked (zero-indexed).

        Returns:
            Boolean showing whether the value was set by the user.

        Raises:
            ValueError: Requested to check an invalid location.
        """

        if row_id not in range(10) or col_id not in range(10):
            raise ValueError("Trying to check invalid rows or columns.")

        original_value = eval("self.sudoku{}[{}][{}]".format(self.board_choice, row_id, col_id))
        if original_value.strip() == "":
            return True
        else:
            return False

    def get_row_numbers(self, row_id, board=[]):
        """Get all numbers from the requested row.
        
        Args:
            row_id (int): The row to return (zero-indexed).
            board (list): The board to check. If none provided, will check the
                current player board.

        Returns:
            A list of integers of the numbers currently in the specificed row.
        """

        if not board:
            board = self.board

        values = []
        for val in board[row_id]:
            if val.strip() != "":
                values.append(int(val))
        return values

    def get_col_numbers(self, col_id, board=[]):
        """Get all numbers from the requested column.
        
        Args:
            col_id (int): The column to return (zero-indexed).
            board (list): The board to check. If none provided, will check the
                current player board.

        Returns:
            A list of integers of the numbers currently in the specificed column.
        """

        if not board:
            board = self.board

        values = []
        for val in list(map(lambda c: c[col_id], board)):
            if val.strip() != "":
                values.append(int(val))
        return values

    def get_grid_numbers(self, row_id, col_id, board=[]):
        """Get all numbers from the 3x3 grid that contains the specified location.

        Args:
            row_id (int): The row to refernce (zero-indexed).
            col_id (int): The column to reference (zero-indexed).
            board (list): The board to check. If none provided, will check the
                current player board.

        Returns:
            A lisr of integers of the numbers currently in the 3x3 grid that 
            contains the location specified.
        """

        if not board:
            board = self.board

        grid_ids = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        row_grid_index = row_id // 3
        col_grid_index = col_id // 3

        values = []
        for row_i in grid_ids[row_grid_index]:
            for col_i in grid_ids[col_grid_index]:
                if board[row_i][col_i].strip() != "":
                    values.append(int(board[row_i][col_i]))
        return values

    def get_possible_numbers(self, row_id, col_id, board=[]):
        """Generates a list of the possible numbers for a location.
        
        Based on the numbers in the locations row, column and grid.

        Args:
            row_id (int): The row of the location to check (zero_indexed).
            col_id (int): The column of the location to check (zero-indexed).

        Returns:
            A list of the possible numbers which can be inserted into the
            specified location.
        """

        if not board:
            board = self.board

        valid_numbers = set(range(1, 10))
        current_row_numbers = set(self.get_row_numbers(row_id, board))
        current_col_numbers = set(self.get_col_numbers(col_id, board))
        current_grid_numbers = set(self.get_grid_numbers(row_id, col_id, board))
        return list(valid_numbers - current_col_numbers - current_row_numbers - current_grid_numbers)

    def row_valid(self, row_id, board=[]):
        """Checks whether the specified row contains the numbers 1-9.
        
        Args:
            row_id (int): The row id to be checked. Zero-indexed.
            board (list): The board to be checked. If none set, will default to
                the player board.

        Returns:
            A boolean representing if the row is valid or not.
        """

        if not board:
            board = self.board
        
        return sorted(list(range(1, 10))) == sorted(self.get_row_numbers(row_id, board))

    def column_valid(self, col_id, board=[]):
        """Checks whether the specified column contains the numbers 1-9.
        
        Args:
            col_id (int): The column id to be checked. Zero-indexed.
            board (list): The board to be checked. If none set, will default to
                the player board.

        Returns:
            A boolean representing if the column is valid or not.
        """

        if not board:
            board = self.board

        return sorted(list(range(1, 10))) == sorted(self.get_col_numbers(col_id, board))

    def grid_valid(self, row_id, col_id, board=[]):
        """Checks whether the grid containing the specified location is valid.

        Note: "Grid" refers to one of the nine 3x3 sub-sections of the board.
        
        Args:
            row_id (int): The row of a cell within the grid to be checked.
                (zero-indexed).
            col_id (int): The column of a cell within the grid to be checked.
                (zero-indexed).
            board (list): The board to be checked. If none set, will default to
                the player board.

        Returns:
            A boolean representing if the grid is valid or not.
        """

        if not board:
            board = self.board

        return sorted(list(range(1, 10))) == sorted(self.get_grid_numbers(row_id, col_id, board))

    def game_state(self, board=[]):
        """Analyses the current state of the game.
        
        Returns:
            A string literal of the current state:
                'in_progress': Game ongoing.
                'game_won': The game has been solved correctly.
                'game_lost': The game has been finished, but is not valid.
                'game_unsolvable': If the game has no solution. Used by the
                    computer_play function if it can't solve a board.
        """

        if not board:
            board = self.board
            player_board = True
        else:
            player_board = False

        game_finished = True
        game_won = True

        for row_id, row in enumerate(board):
            if not self.row_valid(row_id, board):
                game_won = False
            
            if " " in row:
                game_finished = False

            for col_id, value in enumerate(row):
                if not self.column_valid(col_id, board):
                    game_won = False

                if col_id in [0, 3, 6] or row_id in [0, 3, 6]:
                    if not self.grid_valid(row_id, col_id, board):
                        game_won = False

        if self.game_solvable == False:
            if player_board:
                self.game_in_progress = False
            else:
                self.hint_game_in_progress = False
            return "game_unsolvable"

        elif game_finished and game_won:
            if player_board:
                self.game_in_progress = False
                self.game_won = True
            else:
                self.hint_game_in_progress = False
                self.hint_game_won = True
            return "game_won"

        elif game_finished:
            if player_board:
                self.game_in_progress = False
            else:
                self.hint_game_in_progress = False
            return "game_lost"

        else:
            return "in_progress"
    
    def format_preview_grid(self, values, col_header=False):
        """Formats the grid preview for the settings screen.

        Assumes each line will be called individually.
        
        Args:
            values (str): The characters to be analysed and coloured.
            col_header (bool): Whether number characters should be treated and 
                coloured as a row_header. If False, the first number is coloured
                as a row header.
        
        Returns:
            A string containing the original values with colours added.
        """

        ret = []
        col_found = False
        for i in list(values):
            if i.strip() == "":
                ret.append(i)
            elif i.isnumeric():
                if col_header:
                    ret.append("{}{}\u001b[0m".format(self.col_header_colour, i))
                elif not col_found:
                    ret.append("{}{}\u001b[0m".format(self.row_header_colour, i))
                    col_found = True
                else:
                    ret.append("{}{}\u001b[0m".format(self.grid_text_colour, i))
            elif i in ["┏", "━", "┓", "┃", "┗", "┛"]:
                ret.append("{}{}\u001b[0m".format(self.selection_colour, i))
            else:
                ret.append("{}{}\u001b[0m".format(self.grid_colour, i))
        return "".join(ret)

    def print_start_menu(self):
        """Prints out start menu
        
        Note: For consistency the overall menu width must be 71 characters, 
        consisting of a leading space followed by the boxed content. As the 
        border takes 2 characters, this leaves 68 characters of content.
        """

        icon_ascii = [
            "       __               ",
            "      (  ) ,----.__     ",
            "     __||_/___     \    ",
            "    / O||    /|     )   ",
            "   /   ''   / /    /    ",
            "  /________/ /    (     ",
            "  |________|/      \    "
        ]

        title_ascii = [
            "╔═══╗    ╔╗  ╔╗      ╔═══╗          ╔╗    ",
            "║╔═╗║    ║║  ║║      ║╔═╗║          ║║    ",
            "║╚══╦╗╔╦═╝╠══╣║╔╦╗╔╗ ║╚═╝╠╗╔╦═══╦═══╣║╔══╗",
            "╚══╗║║║║╔╗║╔╗║╚╝╣║║║ ║╔══╣║║╠══║╠══║║║║║═╣",
            "║╚═╝║╚╝║╚╝║╚╝║╔╗╣╚╝║ ║║  ║╚╝║║══╣║══╣╚╣║═╣",
            "╚═══╩══╩══╩══╩╝╚╩══╝ ╚╝  ╚══╩═══╩═══╩═╩══╝"
        ]

        Screen.clear()
        # 71 characters (incl. leading space.)
        print(" ╭" + "─" * 68 + "╮")
        print(" │" + Screen.green_text(icon_ascii[0]) + " " * 44 + "│")
        print(" │" + Screen.green_text(icon_ascii[1]) + Screen.magenta_text(title_ascii[0]) + "  │")
        print(" │" + Screen.green_text(icon_ascii[2]) + Screen.magenta_text(title_ascii[1]) + "  │")
        print(" │" + Screen.green_text(icon_ascii[3]) + Screen.magenta_text(title_ascii[2]) + "  │")
        print(" │" + Screen.green_text(icon_ascii[4]) + Screen.magenta_text(title_ascii[3]) + "  │")
        print(" │" + Screen.green_text(icon_ascii[5]) + Screen.magenta_text(title_ascii[4]) + "  │")
        print(" │" + Screen.green_text(icon_ascii[6]) + Screen.magenta_text(title_ascii[5]) + "  │")
        print(" │" + " " * 68 + "│")
        print(" ╰" + "─" * 68 + "╯")
        print((" ╭" + "─" * 20 + "╮ ") * 3) # 3 button tops
        print(" │" + "(P)lay Game".center(20) + "│ ", end="")
        print(" │" + "(S)ettings".center(20) + "│ ", end="")
        print(" │" + "(Q)uit".center(20) + "│")
        print((" ╰" + "─" * 20 + "╯ ") * 3) # 3 button bottoms


    def settings_button(self, option_num, label, value, show_numbers=True):
        """Creates a formatted button for the settings menu, included inside the
        overall settings menu border.

        E.g. ╭───────────────────┬───────────────╮
             │ 1 ┆ Setting Label │ Current Value │
             ╰───────────────────┴───────────────╯

        Args:
            option_num (int): The number a user should press to change the 
                setting. Will be hidden if show_numbers = False
            label (str): The label for the button. Usually the setting 
                description/name.
            value (str): The current value of the setting.
            show_numbers (bool): Whether to show the menu numbers or not. 
                Used to ensure no confusion by the user when any sub-menus appear.

        Returns:
            The formatted button as a string.
        """

        if not show_numbers:
            option_num = " " * len(str(option_num))
        button_label = "{} ┆ {}".format(str(option_num), label)
        button_text = "│ {} │ {} │".format(button_label, value)

        label_width = len(button_label) + 2
        value_width = len(value) + 2

        button = " │  ╭{}┬{}╮".format("─" * label_width, "─" * value_width).ljust(70) + "│\n"
        button += " │  {}".format(button_text).ljust(70) + "│\n"
        button += " │  ╰{}┴{}╯".format("─" * label_width, "─" * value_width).ljust(70) + "│"

        return button

    def print_settings_menu(self, show_numbers=True):
        """Prints the settings menu for the game to the terminal.

        Args:
            show_numbers (bool): Whether or not to render the menu numbers for 
                the user. Recommended to hide numbers in the main menu when 
                rendering sub-menus. Default is True.
        """

        undo_button = self.settings_button(1, 
                                           "Allow undos?",
                                           Screen.human_bool(self.allow_undos),
                                           show_numbers)

        mode_button = self.settings_button(2,
                                           "Game played by",
                                           self.game_mode.title(),
                                           show_numbers)

        input_order_button = self.settings_button(3,
                                                  "Game input order",
                                                  " | ".join(self.game_input_order),
                                                  show_numbers)

        comp_moves_button = self.settings_button(4,
                                                 "Update board as computer solves?",
                                                 Screen.human_bool(self.show_computer_moves),
                                                 show_numbers)

        print(" ╭{}╮".format("─" * 68))
        print(" │{}│".format("Sudoku Puzzle Settings".center(68)))
        print(" │{}│".format("----------------------".center(68)))
        print(" │{}│".format("   Select an option for further information.".ljust(68)))
        print(undo_button)
        print(mode_button)
        print(input_order_button)
        print(comp_moves_button)
        print(" │{}│".format(" " * 68))
        print(" │{}│".format("   Board Colours".ljust(68)))

        grid = [
            self.format_preview_grid("    ╔═══╤═══╤═══╦═".rjust(32)),
            self.format_preview_grid("    ║ 1 │ 2 │ 3 ║ ".rjust(32), True),
            self.format_preview_grid("╔═══╬═══╪═══╪═══╬═".rjust(32)),
            self.format_preview_grid("║ 1 ║ 9 │ 8 │   ║ ".rjust(32)),
            self.format_preview_grid("╟───╫───┏━━━┓───╫─".rjust(32)),
            self.format_preview_grid("║ 2 ║ 7 ┃   ┃ 3 ║ ".rjust(32)),
            self.format_preview_grid("╟───╫───┗━━━┛───╫─".rjust(32)),
            self.format_preview_grid("║ 3 ║   │ 4 │   ║ ".rjust(32)),
            self.format_preview_grid("╠═══╬═══╪═══╪═══╬═".rjust(32)),
        ]

        colour_settings = [
            ["5" if show_numbers else " ", "Grid", self.grid_colour, "".rjust(32)],
            ["6" if show_numbers else " ", "Row Header", self.row_header_colour, "".rjust(32)],
            ["7" if show_numbers else " ", "Column Header", self.col_header_colour, grid[1]],
            ["8" if show_numbers else " ", "Player Text", self.selection_colour, grid[3]],
            ["9" if show_numbers else " ", "Grid Text", self.grid_text_colour, grid[5]],
        ]

        print(" │  ╭{}┬{}╮{}│".format("─" * 25, "─" * 6, " " * 32))

        for i, colours in enumerate(colour_settings):
            print(" │  │ {} ┆ {} │ {}████\u001b[0m │{}│".format(colours[0],
                                                                colours[1].ljust(19),
                                                                colours[2],
                                                                colours[3]))
            grid_section = grid[i * 2 - 2] if i > 0 else "".rjust(32)
            print(" │  ├{}┼{}┤{}│".format("─" * 25, "─" * 6, grid_section))

        Screen.move_up()
        print(" │  ├{}┴{}┤{}│".format("─" * 25, "─" * 6, grid[6].rjust(32)))
        letter = "R" if show_numbers else " "
        label = "Randomise all colours".ljust(26)
        print(" │  │ {} ┆ {} │{}│".format(letter, label, grid[7].rjust(32)))
        print(" │  ╰{}╯{}│".format("─" * 32, grid[8].rjust(32)))
        print(" ├{}┤".format("─" * 68))
        print(" │{}│".format("Enter 'B' or 'Back' to go back".center(68)))
        print(" ╰{}╯".format("─" * 68))

    def ask_for_input(self, prompt, options, pretext=None, merged_head=False):
        """Asks the user for input and validates response.

        Args:
            prompt (str): The question text.
            options (list): List of the valid options a user can respond with.
            pretext (list|str): Any text to preceed the question. Multiple lines
                of text can be displayed by passing in a list.
            merged_head (bool): Whether to print the top line or not. Useful for
                attaching the input request to a previouslt printed header menu.

        Returns:
            String of the validated user input in lowercase.
        """

        valid_values = list(map(lambda x: str(x).lower(), options))
        if not merged_head:
            print(" ╭{}╮".format("─" * 68))

        if isinstance(pretext, str):
            pretext = [pretext]

        if pretext:
            for line in pretext:
                print(" │ {} │".format(line.ljust(66)))

        print(" │{}│\u001b[0K".format(" " * 68))
        print(" ╰{}╯\u001b[0J".format("─" * 68))
        Screen.move_up(2)
        while True:
            user_input = input(" │ {}: ".format(prompt)).lower().strip()
            if user_input not in valid_values:
                error_text = Screen.print_error("'{}' isn't valid. Please try again.".format(user_input))
                print(" ╰{}╯\u001b[0J".format("─" * 68))
                Screen.move_up(error_text.count('\n') + 2)
                print(" │{}│\u001b[0K".format(" " * 68))
                Screen.move_up(1)
                continue
            else:
                return user_input
    
    def settings(self):
        """Clears the screen and renders a graphical interace to allow the user 
        to edit game settings.
        """
        
        while True:
            Screen.clear()
            self.print_settings_menu()
            user_input = self.ask_for_input("Choose a setting to update",
                                            list(range(1,10)) + ["b", "back", "r", "q", "quit"])

            if user_input == "1":
                Screen.move_up(2)
                user_input = self.ask_for_input("Choose (Y)es or (N)o",
                                                ["y", "n", "yes", "no", "b", "back"],
                                                "When playing, do you want to be allowed to undo your moves?")
                if user_input in ["y", "yes"]:
                    self.allow_undos = True
                elif user_input in ["b", "back"]:
                    continue
                else:
                    self.allow_undos = False

            elif user_input == "2":
                Screen.move_up(2)
                user_input = self.ask_for_input("Choose (P)layer or (C)omputer",
                                                ["p", "c", "player", "computer", "b", "back"],
                                                ["Should the game be solved by you or the computer?",
                                                "Note: You can ask the computer to solve the game while playing."])

                if user_input in ["p", "player"]:
                    self.game_mode = "player"
                elif user_input in ["b", "back"]:
                    continue
                else:
                    self.game_mode = "computer"

            elif user_input == "3":
                Screen.move_up(2)
                user_input = self.ask_for_input("Enter order using R, C & V",
                                                ["rcv", "crv", "vcr", "vrc", "rvc", "cvr", "d", "default", "b", "back"],
                                                ["Change the order you're asked for input.",
                                                 "Enter R for row, C for column and V for value. E.g. \"crv\".",
                                                 "If you'd like the default order, you can enter D to reset it.", ""])

                if user_input in ["b", "back"]:
                    continue
                elif user_input == "d":
                    user_input = "rcv"

                order = []
                for val in user_input:
                    if val == "r":
                        order.append("row")
                    elif val == "c":
                        order.append("column")
                    elif val == "v":
                        order.append("value")
                
                self.game_input_order = order

            elif user_input == "4":
                Screen.move_up(2)
                user_input = self.ask_for_input("Choose (Y)es or (N)o",
                                                ["y", "n", "yes", "no", "b", "back"],
                                                ["Should the board refresh as the computer tries solving the game?",
                                                 "Note: This will cause the solve to be slower, but is fun to watch."])
                
                if user_input in ["y", "yes"]:
                    self.show_computer_moves = True
                elif user_input in ["b", "back"]:
                    continue
                else:
                    self.show_computer_moves = False

            elif user_input in ["5", "6" ,"7" ,"8", "9"]:
                Screen.clear()
                self.print_settings_menu(False)

                setting_mappings = {
                    "5": "grid_colour",
                    "6": "row_header_colour",
                    "7": "col_header_colour",
                    "8": "selection_colour",
                    "9": "grid_text_colour",
                }

                self.ask_and_set_colour(setting_mappings[user_input])

            elif user_input == "r":
                possible_colours = self.colour_options.copy()

                self.grid_colour = random.choice(possible_colours)
                possible_colours.remove(self.grid_colour)

                self.row_header_colour = random.choice(possible_colours)
                possible_colours.remove(self.row_header_colour)

                self.col_header_colour = random.choice(possible_colours)
                possible_colours.remove(self.col_header_colour)

                self.selection_colour = random.choice(possible_colours)
                possible_colours.remove(self.selection_colour)

                self.grid_text_colour = random.choice(possible_colours)
            
            elif user_input in ["b", "back"]:
                return
            
            elif user_input in ["q", "quit"]:
                Screen.move_up(2)
                pretext = "Are you sure you want to Quit?"
                confirmation = self.ask_for_input("(Y)es or (N)o", ["y", "n", "yes", "no"], pretext)
                if confirmation in ["y", "yes"]:
                    self.exit_game()

    def ask_and_set_colour(self, setting):
        """Renders a menu to the user to choose a colour and updates the related
        colour setting.

        Also allows user to return using "b" or "back".
        
        Args:
            setting (str): The setting to be updated.

        Raises:
            ValueError: Trying to set an invalid setting.
        """

        heading_mappings = {
            "grid_colour": "Grid Colour",
            "row_header_colour": "Row Header Colour",
            "col_header_colour": "Column Header Colour",
            "selection_colour": "Player Text Colour",
            "grid_text_colour": "Grid Text Colour",
        }

        if setting not in heading_mappings:
            raise ValueError("Trying to set invalid setting.")

        current_colour = eval("self.{}".format(setting))
        print(" ╭{}╮".format("─" * 68))
        print(" │{}│".format(("Change " + heading_mappings[setting]).center(68)))
        print(" ├────────{}┤\n ".format("┬─────────" * 6, ), end="")
        for i, colour in enumerate(self.colour_options):
            if i in [0, 7]:
                width = 2
            else:
                width = 3
            
            if i == 7:
                print("│\n ├────────{}┤\n ".format("┼─────────" * 6, ), end="")
            
            indicator = "▚▚▚▚" if current_colour == colour else "████"
            print("│ " + colour + str(i + 1).ljust(width) + indicator + "\u001b[0m ", end="")

        print("│\n ├────────{}┤".format("┴─────────" * 6))
        user_input = self.ask_for_input("Enter a colour number (current is checkered)",
                                         list(range(1, 15)) + ['b', 'back'],
                                         merged_head=True)
        if user_input in ["b", "back"]:
            return
        else:
            # Update the setting with the chosen colour - using exec() here, however 
            # this is considered safe as the setting variable name is validated above.
            exec("self.{} = self.colour_options[int(user_input) - 1]".format(setting))

    def log_move(self, row_id, col_id, value):
        """Logs the game moves made.
        
        Args:
            row_id (int): The row of the updated location (zero-indexed).
            col_id (int): The column of the updated location (zero-indexed).
            value (str): The value updated, or "X" to indicate an invalid move.
        """

        self.move_history.append([
            row_id,
            col_id,
            value,
            time.time()
        ])

    def get_latest_move(self):
        """Gets the latest move the player made.
        
        Returns:
            A list containing:
            - row_id
            - col_id
            - value
            - seconds since epoch
        """

        if not self.move_history:
            return []
        
        return self.move_history[len(self.move_history) - 1]

    def revert_move(self, number_of_moves=1):
        """Revert's player made moves, leaving hints on the board.

        Dev note: Ensure to refresh the board after use as this function only
        removes the moves from the board. It does NOT update the UI.

        Args:
            number_of_moves (int): The number of moves to undo. Defaults to 1.

        Returns:
            Number of moves actually undone. Will be less than input if that 
            many moves hasn't been played yet. 
        """

        counter = 0

        for i in range(int(number_of_moves)):
            if self.move_history:
                move = self.move_history.pop()
                self.update_board(move[0], move[1], " ")
                counter += 1
        
        return counter

    def start(self):
        """Shows the start menu asking user what they want to do."""

        while True:
            while self.game_in_progress == False:
                self.print_start_menu()
                menu_choice = self.ask_for_input("Enter a menu option (P, S or Q)",
                                                 ["p", "s", "q"])
                
                if menu_choice == "p":
                    Screen.move_up(2)
                    menu_choice = self.ask_for_input("Choose a game (1, 2, 3 or 4)",
                                                     list(range(1, 5)) + ["b", "back"])

                    if menu_choice in ["b", "back"]:
                        continue

                    self.set_board(int(menu_choice))
                    self.game_in_progress = True
                    self.start_timer(True)

                elif menu_choice == "s":
                    self.settings()

                elif menu_choice == "q":
                    Screen.move_up(2)
                    pretext = "Are you sure you want to Quit?"
                    confirmation = self.ask_for_input("(Y)es or (N)o", ["y", "n", "yes", "no"], pretext)
                    if confirmation in ["y", "yes"]:
                        self.exit_game()
                    else:
                        continue

            self.print_board()
            self.human_play()
    
    def print_board(self, selected_row=0, selected_col=0):
        """Prints the sudoku board, including right-panel with keyboard shortcuts.
        
        Args:
            selected_row (int): The row of the cell to highlight.
            selected_col (int): The column of the cell to highlight.
        """

        sudoku = self.board
        selected_row -= 1
        selected_col -= 1

        last_move = self.get_latest_move()
        last_move_row = str(last_move[0] + 1) if last_move else ""
        last_move_col = str(last_move[1] + 1) if last_move else ""
        last_move_value = str(last_move[2]) if last_move else ""
        text_reset = "\u001b[0m"

        Screen.clear()

        # GRID HEADERS
        # ------------
        print(" ╭{}╮".format("─" * 68))
        print(" │{}{}{}│".format(self.col_header_colour.rjust(len(self.col_header_colour) + 7),
                                 "C O L U M N S".center(37),
                                 "\u001b[0m".ljust(28)))
        print(" │{}╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗{}│".format(self.grid_colour.rjust(len(self.grid_colour) + 7),
                                                                    text_reset.ljust(28)))

        print(" │{}║{}".format(self.grid_colour.rjust(len(self.grid_colour) + 7),
                               text_reset), end="")

        # Print column labels with only numbers in colour.
        for i in range(1,10):
            print(f" { self.col_header_colour }{ i }{ text_reset } ", end="")
            if i in [3, 6]:
                print(f"{ self.grid_colour }║{ text_reset }", end="")
            elif i == 9:
                print(f"{ self.grid_colour }║{ text_reset }   SUDOKU { self.board_choice } PUZZLE      │")
            else:
                print(f"{ self.grid_colour }│{ text_reset }", end="")

        print(f" │   { self.grid_colour }╔═══╬═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣{ text_reset }   ---------------      │")

        # GRID BODY
        # ---------
        for row_id in range(9):
            # Output row label on square rows.
            if row_id == 4:
                print(f" │{ self.row_header_colour } O { text_reset }", end="")
            elif row_id == 5:
                print(f" │{ self.row_header_colour } S { text_reset }", end="")
            else:
                print(" │   ", end="")

            # Print row numbers
            print(f"{ self.grid_colour }║{ text_reset }", end="")
            print(f"{ self.row_header_colour } { row_id + 1 } { text_reset }", end="")
            print(f"{ self.grid_colour }║{ text_reset }", end="")

            # Print board row
            for col_id, val in enumerate(self.board[row_id]):
                if self.user_entered(row_id, col_id):
                    print(self.selection_colour, end="")
                else:
                    print(self.grid_text_colour, end="")
                
                print(f" { str(val) } { text_reset }", end="")

                if col_id in [2, 5, 8]:
                    divider = "║"
                else:
                    divider = "│"
                
                print(self.grid_colour + divider + text_reset, end="")

            # Sidebar for square rows.
            if self.game_in_progress:
                if row_id == 1:
                    print(f"   { '--------------'.ljust(21) }│")
                elif row_id == 2:
                    print(f"   { ('Column : ' + last_move_col).ljust(21) }│")
                elif row_id == 5:
                    print(f"   { '------------------'.ljust(21) }│")
                elif row_id == 6:
                    print(f"   { 'H = Hint'.ljust(21) }│")
                elif row_id == 7:
                    print(f"   { 'S = Settings'.ljust(21) }│")
                elif row_id == 8:
                    print(f"   { 'Q = Quit (exit)'.ljust(21) }│")
                else:
                    print(" " * 24 + "│")
            else:
                print(" " * 24 + "│")

            # Output row label on divider rows.
            if row_id == 3:
                print(f" │{ self.row_header_colour } R { text_reset }", end="")
            elif row_id == 4:
                print(f" │{ self.row_header_colour } W { text_reset }", end="")
            else:
                print(" │   ", end="")

            # Output dividers.
            if row_id in [2, 5]:
                print(f"{ self.grid_colour }╠═══╬═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣{ text_reset }", end="")
            elif row_id < 8:
                print(f"{ self.grid_colour }╟───╫───┼───┼───╫───┼───┼───╫───┼───┼───╢{ text_reset }", end="")
            else:
                print(f"{ self.grid_colour }╚═══╩═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝{ text_reset }{ ' ' * 24 }│", end="")

            # Sidebar for divider rows.
            if self.game_in_progress:
                if row_id == 0:
                    print(f"   { 'Last User Move'.ljust(21) }│")
                elif row_id == 1:
                    print(f"   { ('Row    : ' + last_move_row).ljust(21) }│")
                elif row_id == 2:
                    print(f"   { ('Value  : ' + last_move_value).ljust(21) + text_reset }│")
                elif row_id == 4:
                    print(f"   { 'Keyboard Shortcuts'.ljust(21) }│")
                elif row_id == 5 and self.allow_undos:
                    print(f"   { 'U = Undo Move(s)'.ljust(21) }│")
                elif row_id == 6:
                    print(f"   { 'C = Computer Solve'.ljust(21) }│")
                elif row_id == 7:
                    print(f"   { 'M = Main Menu'.ljust(21) }│")
                elif row_id == 8:
                    print(f"\n ╰{'─' * 68}╯")
                else:
                    print(" " * 24 + "│")
            elif row_id == 8:
                print(f"\n ╰{'─' * 68}╯")
            else:
                print(" " * 24 + "│")

            # Add highlight if needed.
            if selected_row == row_id and selected_col >= 0:
                Screen.move_up(3)
                if row_id == 8:
                    Screen.move_up()
                Screen.move_right(9 + (selected_col * 4))
                print(f"{ self.selection_colour }┏━━━┓{ text_reset }")
                Screen.move_right(9 + (selected_col * 4))
                print(f"{ self.selection_colour }┃{ text_reset }", end="")
                Screen.move_right(3)
                print(f"{ self.selection_colour }┃{ text_reset }")
                Screen.move_right(9 + (selected_col * 4))
                print(f"{ self.selection_colour }┗━━━┛{ text_reset }")
                if row_id == 8:
                    Screen.move_down()

    def get_value(self, row_id, col_id):
        """Gets a value from a location on the board.
        
        Args:
            row_id (int): The row of the required location (zero-indexed).
            col_id (int): The column of the required location (zero-indexed).

        Returns:
            A string of the value at the specified location.
            Empty cells return an empty string.
        """

        return self.board[row_id][col_id].strip()

    def print_lost_message(self):
        """Prints a 'Game Lost' message to the terminal."""

        print(" ╭{}╮".format("─" * 68))
        print(" │{}│".format(Screen.red_text("   ______                        __               __ ".center(68))))
        print(" │{}│".format(Screen.red_text("  / ____/___ _____ ___  ___     / /   ____  _____/ /_".center(68))))
        print(" │{}│".format(Screen.red_text(" / / __/ __ `/ __ `__ \/ _ \   / /   / __ \/ ___/ __/".center(68))))
        print(" │{}│".format(Screen.red_text("/ /_/ / /_/ / / / / / /  __/  / /___/ /_/ (__  ) /_  ".center(68))))
        print(" │{}│".format(Screen.red_text("\____/\__,_/_/ /_/ /_/\___/  /_____/\____/____/\__/  ".center(68))))
        print(" │{}│".format(" " * 68))
        print(" │{}│".format("Oh no! Don't worry. Why not try again?".center(68)))
        text = "You made {} moves taking {}.".format(self.number_of_moves, Screen.human_duration(self.game_time))
        timing = Screen.wrap_string(text, 66, "center")
        timing = timing.replace("\n", "\n\u001b[3C") # Move the cursor so it doesn't print over the borders.
        line_count = timing.count("\n") + 1

        for i in range(line_count):
            print(" │{}│\u001b[0K".format(" " * 68))
        
        Screen.move_up(line_count)
        print(" │ " + timing)
        print(" ╰{}╯\u001b[0J".format("─" * 68))

    def print_won_message(self):
        """Prints a 'Game Won' message to the terminal."""

        print(" ╭{}╮".format("─" * 68))
        print(" │{}│".format(Screen.green_text("   ______                        _       __          ".center(68))))
        print(" │{}│".format(Screen.green_text("  / ____/___ _____ ___  ___     | |     / /___  ____ ".center(68))))
        print(" │{}│".format(Screen.green_text(" / / __/ __ `/ __ `__ \/ _ \    | | /| / / __ \/ __ \\".center(68))))
        print(" │{}│".format(Screen.green_text("/ /_/ / /_/ / / / / / /  __/    | |/ |/ / /_/ / / / /".center(68))))
        print(" │{}│".format(Screen.green_text("\____/\__,_/_/ /_/ /_/\___/     |__/|__/\____/_/ /_/ ".center(68))))
        print(" │{}│".format(" " * 68))
        if self.game_mode == 'player':
            print(" │{}│".format("Woah - look at you go! Why not try another game?".center(68)))
        else:
            print(" │{}│".format("Computer did good! Why not try another game?".center(68)))
        print(" │{}│".format(" " * 68))
        text = "The game was solved in {} moves taking {}.".format(self.number_of_moves, Screen.human_duration(self.game_time))
        timing = Screen.wrap_string(text, 66, "center")
        timing = timing.replace("\n", "\n\u001b[3C") # Move the cursor so it doesn't print over the borders.
        line_count = timing.count("\n") + 1

        for i in range(line_count):
            print(" │{}│\u001b[0K".format(" " * 68))
        
        Screen.move_up(line_count)
        print(" │ " + timing)
        print(" ╰{}╯\u001b[0J".format("─" * 68))

    def print_unsolvable_message(self):
        """Prints a "Can't solve this board" message to the terminal.
        
        Used by computer_play() when the board cannot be solved.
        """

        print(" ╭{}╮".format("─" * 68))
        print(" │{}│".format(Screen.blue_text(" _       ____                          ".center(68))))
        print(" │{}│".format(Screen.blue_text("| |     / / /_  ____  ____  ____  _____".center(68))))
        print(" │{}│".format(Screen.blue_text("| | /| / / __ \/ __ \/ __ \/ __ \/ ___/".center(68))))
        print(" │{}│".format(Screen.blue_text("| |/ |/ / / / / /_/ / /_/ / /_/ (__  ) ".center(68))))
        print(" │{}│".format(Screen.blue_text("|__/|__/_/ /_/\____/\____/ .___/____/  ".center(68))))
        print(" │{}│".format(Screen.blue_text("                        /_/            ".center(68))))
        print(" │{}│".format(" " * 68))
        print(" │{}│".format("Well this is awkward :/ Looks like I can\'t solve this for you.".center(68)))
        text = "The game was confirmed unsolvable in {} moves taking {}.".format(self.number_of_moves, Screen.human_duration(self.game_time))
        timing = Screen.wrap_string(text, 66, "center")
        timing = timing.replace("\n", "\n\u001b[3C") # Move the cursor so it doesn't print over the borders.
        line_count = timing.count("\n") + 1

        for i in range(line_count):
            print(" │{}│\u001b[0K".format(" " * 68))
        
        Screen.move_up(line_count)
        print(" │ " + timing)
        print(" ╰{}╯\u001b[0J".format("─" * 68))

    def exit_game(self):
        """Clears the screen, prints a goodbye message, and exits the program."""

        Screen.clear()
        self.print_start_menu()
        Screen.move_up(4)
        print(" │{}│".format(" " * 68))
        print(" │{}│\u001b[0K".format("Thanks for playing. See you again soon!".center(68)))
        print(" │{}│".format(" " * 68))
        print(" ╰{}╯\u001b[0J".format("─" * 68))
        exit()
    
    def is_valid(self, row_id, col_id):
        """Checks whether a move can be made by the player.
        
        Args:
            row_id (int): The row to be checked (zero-indexed).
            col_id (int): The column to be checked (zero-indexed).

        Returns:
            A boolean whether the chosen move is valid.
        """

        return self.get_value(row_id, col_id) == ""

    def human_play(self):
        """Runs a game of Sudoku for the player.
        
        Also handles all management of the in-game keyboard shortcuts.
        """

        while True:
            while self.game_state() == "in_progress":
                if self.game_mode == "computer":
                    self.computer_play()
                    self.print_board()
                    break

                request_items = self.game_input_order
                request_values = [0] * 3
                row, col, value = 0, 0, 0
                for i, request in enumerate(request_items):
                    valid_values = list(range(1, 10)) + ["h", "s", "c", "m", "q", "u", "b"]
                    pretext = []
                    if i >= 1:
                        pretext.append("Enter {}: {}".format(request_items[0], str(request_values[0])))
                    
                    if i > 1:
                        pretext.append("Enter {}: {}".format(request_items[1], str(request_values[1])))

                    user_input = self.ask_for_input("Enter {}".format(request), valid_values, pretext)

                    # Check and process keyboard shortcuts.
                    if user_input in ["m", "b"]:
                        Screen.move_up(i + 2)
                        pretext = "Go back to the main menu (ending your current game)?"
                        confirmation = self.ask_for_input("Enter (Y)es or (N)o", ["Y", "N", "yes", "no"], pretext)
                        if confirmation in ["y", "yes"]:   
                            self.game_in_progress = False
                            return
                        elif confirmation in ["n", "no"]:
                            Screen.clear()
                            self.print_board()
                            break
                    
                    elif user_input == "h":
                        hint_row, hint_col, hint_value = self.get_hint()
                        Screen.clear()
                        self.print_board(hint_row + 1, hint_col + 1)
                        print(" ╭{}╮".format("─" * 68))
                        print(" │{}│".format(" " * 68))
                        print(" ╰{}╯\u001b[0J".format("─" * 68))
                        Screen.move_up(2)
                        text = " │ {} entered into row {}, column {} for you. Press any key."
                        input(text.format(hint_value, str(hint_row + 1), str(hint_col + 1)))
                        Screen.move_up(2)
                        break

                    elif user_input == "q":
                        Screen.move_up(i + 2)
                        pretext = "Are you sure you want to Quit?"
                        confirmation = self.ask_for_input("(Y)es or (N)o", ["y", "n", "yes", "no"], pretext)
                        if confirmation in ["y", "yes"]:
                            self.exit_game()
                        else:
                            Screen.clear()
                            self.print_board()
                            break
                    
                    elif user_input == "s":
                        self.stop_timer()
                        self.settings()
                        Screen.clear()
                        self.start_timer()
                        self.print_board()
                        break

                    elif user_input == "u":
                        if not self.allow_undos:
                            Screen.move_up(2)
                            print(" ╭{}╮".format("─" * 68))
                            print(" │{}│".format(" Sorry, undos aren't allowed. You can change this in settings. ".ljust(68)))
                            print(" │{}│".format(" " * 68))
                            print(" ╰{}╯\u001b[0J".format("─" * 68))
                            Screen.move_up(2)
                            input(" │ Press any key to continue....")
                            Screen.move_up(3)
                        elif not self.move_history:
                            Screen.move_up(2)
                            print(" ╭{}╮".format("─" * 68))
                            print(" │{}│".format(" " * 68))
                            print(" ╰{}╯\u001b[0J".format("─" * 68))
                            Screen.move_up(2)
                            input(" │ You've not made any moves yet! Press any key to continue....")
                            Screen.move_up(2)
                        else:
                            Screen.move_up(2)
                            number_of_moves = self.ask_for_input("How many moves would you like to undo?",
                                                                list(range(1,1000)))

                            undos_actioned = self.revert_move(number_of_moves)
                            Screen.clear()
                            self.print_board()
                            print(" ╭{}╮".format("─" * 68))
                            print(" │{}│".format(" " * 68))
                            print(" ╰{}╯\u001b[0J".format("─" * 68))
                            Screen.move_up(2)

                            if int(number_of_moves) == undos_actioned:
                                plural = "s" if int(undos_actioned) > 1 else ""
                                input(" │ {} move{} undone. Press any key to continue...".format(undos_actioned, plural))
                            else:
                                input(" │ All moves undone. Press any key to continue...")
                            Screen.move_up(2)
                        break
                    
                    elif user_input == "c":
                        self.game_mode = "computer"
                        break

                    # Handles playing the game.
                    if request == "row":
                        row = int(user_input)
                        request_values[i] = row

                    elif request == "column":
                        col = int(user_input)
                        request_values[i] = col
                    
                    else:
                        value = user_input
                        request_values[i] = value

                    if col and row and not self.is_valid(row - 1, col - 1):
                        print(" ╭{}╮".format("─" * 68))
                        print(" │ Enter row: {}│".format(str(row).ljust(56)))
                        print(" │ Enter column: {}│".format(str(col).ljust(53)))
                        Screen.print_error("Location isn't empty. Press enter to try again.")
                        print(" ╰{}╯\u001b[0J".format("─" * 68))
                        input()
                        Screen.clear()
                        self.print_board()
                        break

                    if col and row and value:
                        self.update_board(row - 1, col - 1, value)
                        self.log_move(row - 1, col - 1, value)
                        self.number_of_moves += 1
                        Screen.clear()
                        self.print_board()
                        if self.game_state() != "in_progress":
                            self.stop_timer()
                            break
                    else:
                        Screen.clear()
                        self.print_board(row, col)
            
            else:
                if self.game_state() == "game_won":
                    self.print_won_message()
                elif self.game_state() == "game_lost":
                    self.print_lost_message()
                elif self.game_state() == "game_unsolvable":
                    self.print_unsolvable_message()
                
                if self.game_mode == 'computer':
                    self.game_mode = "player"
                
                print(" ╭────────────────────╮ " * 3)
                print(" │{}│ ".format("(P)lay Again".center(20)), end="")
                print(" │{}│ ".format("(R)andom Game".center(20)), end="")
                print(" │{}│ ".format("(M)ain Menu".center(20)))
                print(" ╰────────────────────╯ " * 3)

                menu_choice = self.ask_for_input("Choose a menu option (P, R or M)",
                                                ["p", "r", "m", "b", "q", "h", "s"])
            
                # Handle post game options.
                if menu_choice == "p":
                    self.set_board(self.board_choice)
                    self.game_in_progress = True
                    self.game_won = False
                    self.start_timer(True)
                    Screen.clear()
                    self.print_board()
                    break

                elif menu_choice == "r":
                    game_choices = list(range(1, 5))
                    game_choices.remove(self.board_choice)
                    self.board_choice = random.choice(game_choices)
                    self.set_board(self.board_choice)
                    self.game_in_progress = True
                    self.game_won = False
                    self.start_timer(True)
                    Screen.clear()
                    self.print_board()

                elif menu_choice in ["m", "b"]:
                    return

                elif menu_choice == "q":
                    Screen.move_up(2)
                    pretext = "Are you sure you want to Quit?"
                    confirmation = self.ask_for_input("(Y)es or (N)o", ["y", "n", "yes", "no"], pretext)
                    if confirmation in ["y", "yes"]:
                        self.exit_game()
                    else:
                        Screen.clear()
                        self.print_board()
                    
                elif menu_choice == "s":
                    self.settings()
                    Screen.clear()
                    self.print_board()

    def board_full(self, board=[]):
        """Returns whether the board is full or not.
        
        Args:
            board (list): Which board to check. If left blank, will check the
                players game board.

        Returns:
            Boolean of whether the board is full or not.
        """

        if not board:
            board = self.board

        for row in board:
            for value in row:
                if value.strip() == "":
                    return False
        return True

    def get_hint(self):
        """Solves the initial board and then returns a clue.
        
        Checks the current state of the board to ensure it returns a clue for a
        currently empty cell. Also stores the solution once found to give hints
        faster if used again.
        """

        if self.solved_board:
            solution = self.solved_board
        else:
            solution = []
            possible_numbers = self.get_possible_numbers_list(self.hint_board)
            self.computer_move(self.hint_board, possible_numbers, solution, False)
            self.solved_board = solution
        
        empty_cells = self.get_possible_numbers_list()
        hint_row = empty_cells[0][0]
        hint_col = empty_cells[0][1]
        hint_value = solution[0][hint_row][hint_col]
        self.update_board(hint_row, hint_col, int(hint_value))

        return [hint_row, hint_col, hint_value]

    def computer_move(self, board, possible_numbers_list, solution=[], print_output=True, i=0):
        """Makes a move based on the valid numbers available. Prioritises cells
        with fewer possible options to ensure it has a higher chance of choosing
        the correct option. Is used for both solving a board for the player, as 
        well as solving the board to provide hints.

        Note: This function is recursive and will keep running until either:
            1. A valid solution to the board has been found
            2. It has tried every possible solution for all empty cells.

        Args:
            board (list): The board to be solved.
            possible_number_list (list): A list of cells with their current
                possible valid inputs.
            solution (list): Initially empty, is a placeholder to ensure recursion
                returns and exits once a solution is found.
            print_output (bool): Whether to print the output to the screen or not.
            i (int): An iterator used to calculate a "calculating" output to the
                player when working.
        """
        if len(solution):
            return

        location_row_id = possible_numbers_list[0][0]
        location_col_id = possible_numbers_list[0][1]

        possible_numbers = self.get_possible_numbers(location_row_id, location_col_id, board)
        for number in possible_numbers:

            self.update_board(location_row_id, location_col_id, number, board)

            # This is used to ensure that if the computer is solving the game
            # board on the players behalf, moves still increase.
            if print_output:
                self.number_of_moves += 1

            if self.show_computer_moves and print_output:
                self.print_board()
            else:
                print(f' ╰{"─" * 68}╯\u001b[0J')
                Screen.move_up(2)
                i = i + 1 if i < 10 else 1
                print(" │" + (" Computer calculating" + "." * i).ljust(68) + "│")

            if self.board_full(board):
                if self.game_state(board) != "in_progress":
                    solution.append(board)
                    return

            locations = self.get_possible_numbers_list(board)

            if len(locations) > 0:
                if locations[0][3] != 0:
                    self.computer_move(board, locations, solution, print_output, i+1)

            if len(solution):
                return

            self.update_board(location_row_id, location_col_id, " ", board)
            
    def update_possible_numbers(self, board=[]):
        """Generates a list of possible numbers left and saves these.
        
        Args:
            board (list): The board to check. If none set, will be set to the 
                players current board.
        """

        if not board:
            board = self.board
            player_board = True
        else:
            player_board = False

        for row_id, row in enumerate(board):
            for col_id, value in enumerate(row):
                if player_board and value.strip() == '':
                    self.possible_numbers[row_id][col_id] = self.get_possible_numbers(row_id, col_id)
                elif player_board:
                    self.possible_numbers[row_id][col_id] = [0]
                elif value.strip() == '':
                    self.hint_possible_numbers[row_id][col_id] = self.get_possible_numbers(row_id, col_id, board)
                else:
                    self.hint_possible_numbers[row_id][col_id] = [0]
    
    def get_possible_numbers_list(self, board=[]):
        """Returns an ordered list of all empty cells with their remaining 
        possible numbers, including empty cells with 0 valid numbers possible.

        Args:
            board (list): The board to analyse. If none set, will be set to the
                players currentl board.

        Returns:
            A list of all cells with their possible numbers, sorted ascending
            based on the number of possible valid numbers left.
            Outputs each cell as a list containing:
                - row_id
                - col_id
                - list of possible valid numbers
                - the count of valid numbers for the cell
        """

        if not board:
            board = self.board
            player_board = True
        else:
            player_board = False
        
        if player_board:
            self.update_possible_numbers()
        else:
            self.update_possible_numbers(board)
        ret = []

        if player_board:
            possible_numbers = self.possible_numbers
        else:
            possible_numbers = self.hint_possible_numbers

        for row_id, cols in enumerate(possible_numbers):
            for col_id, values in enumerate(cols):
                if values == [0]:
                    continue
                ret.append([row_id, col_id, values, len(values)])

        return sorted(ret, key=lambda x: x[3])

    def computer_play(self):
        """Kicks off the recursion for the computer to try solving the board."""

        self.computer_move(self.board, self.get_possible_numbers_list(), [])
        if self.game_state() == 'in_progress':
            self.game_solvable = False
        self.stop_timer()

if __name__ == "__main__":
    Screen.ansi_compatibility_check()
    game = Sudoku()
    game.start()