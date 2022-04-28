from interpreter.tokens import *
from console.error import *


# Writing this sucked...
class lexer:
    """
    Lexer class.
    """

    def tokenize(code: "list[str]") -> "list[str]":
        """
        Tokenizes `code` for the parser.
        """

        # Variables #

        # INTS #
        c: int = 0  # Counter.
        squote_count: int = 0
        dquote_count: int = 0

        # STRINGS #
        section: str = ""
        command: str = ""
        variable: str = ""
        value: str = ""
        string: str = ""

        # BOOLEANS #
        paren_open: bool = False
        brack_open: bool = False
        brace_open: bool = False
        single_quote_open: bool = False
        double_quote_open: bool = False
        right_of_eqs: bool = False
        commented: bool = False
        error_on_invalid_token: bool = False

        # DICTIONARIES #
        var_dict: "dict[str, str]" = {}
        task_dict: "dict[str, list[str]]" = {}

        # Looping through every character in `code`.
        while c < len(code):
            if code[c] == WHITESPACE or TAB:
                c += 1
            elif code[c] == COMMENT:
                print("COMMENT")
                while not code[c] == LINEFEED:
                    c += 1
            elif code[c] in LOWER_LETTER or code[c] in UPPER_LETTER:
                print(code[c])

            c += 1
