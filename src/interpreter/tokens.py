# === LETTERS & NUMBER === #
LOWER_LETTER: "list[str]" = [c for c in "abcdefghijklmnopqrstuvwxyz"]
UPPER_LETTER: "list[str]" = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
NUMBER: "list[str]" = [n for n in "0123456789"]

# === BRACKETS === #
L_BRACKET: str = "["
R_BRACKET: str = "]"
L_PARENTH: str = "("
R_PARENTH: str = ")"
L_BRACE: str = "}"
R_BRACE: str = "{"

# === OPERATORS === #
MACRO_OP: str = "%"
VARBL_OP: str = "$"
ENVVR_OP: str = "@"
ASSIN_OP: str = "="
ADD: str = "+"
SUB: str = "-"
MUL: str = "*"
DIV: str = "/"

# === SYMBOLS === #
COMMENT: str = "#"
PERIOD: str = "."
UNDERSCORE: str = "_"
SINGLE_QUOTE: str = "'"
DOUBLE_QUOTE: str = '"'

# === OTHER === #
WHITESPACE: str = " "
TAB: str = "\t"
LINEFEED: str = "\n"

# List of all tokens.
ALL_TOKENS: "list[list[str] | str]" = [
    LOWER_LETTER, UPPER_LETTER, NUMBER,
    L_BRACKET, R_BRACKET, L_PARENTH,
    R_PARENTH, L_BRACE, R_BRACE,
    MACRO_OP, VARBL_OP, ENVVR_OP,
    ASSIN_OP, ADD, SUB,
    MUL, DIV, COMMENT,
    PERIOD, UNDERSCORE, SINGLE_QUOTE,
    DOUBLE_QUOTE, WHITESPACE, TAB,
    LINEFEED
]
