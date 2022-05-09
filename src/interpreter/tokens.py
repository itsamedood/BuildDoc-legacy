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
MACRO_OP: str = "%"  # For calling macros.
VARBL_OP: str = "$"  # For using variables declared in `.VARS`.
ENVVR_OP: str = "@"  # For using env. vars.
SYSTM_OP: str = "?"  # For getting information like OS name.
ASSIN_OP: str = "="  # For creating variables.

# === SYMBOLS === #
COMMENT: str = "#"
DOUBLE_QUOTE: str = '"'
SINGLE_QUOTE: str = "'"
PERIOD: str = "."
COMMA: str = ","
UNDERSCORE: str = "_"

# === OTHER === #
WHITESPACE: str = " "
TAB: str = "\t"
LINEFEED: str = "\n"

# === LISTS === #
ALL_OPERATORS: "list[str]" = [
    MACRO_OP, VARBL_OP, ENVVR_OP,
    SYSTM_OP, ASSIN_OP
]
