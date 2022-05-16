from console.color import color
from sys import exit

BOLD_WHITE = color.ansi(1, 37)
BOLD_GRAY = color.ansi(1, 39)


class builddoc_base_error(BaseException):
    """
    Base class for BuildDoc errors and such.
    """

    def __init__(self, message: str, code: int = 1) -> None:
        print(
            f"builddoc: {color.ERROR}error{BOLD_WHITE}: {BOLD_WHITE}: {message}{color.RESET}")
        exit(code)


class builddoc_error(builddoc_base_error):
    """
    Represents an error from BuildDoc, whether it be internal or caused by the user.
    """

    def __init__(self, message: str, line: int, character: int, code: int = 1) -> None:
        print(
            f"builddoc: {color.ERROR}error{BOLD_WHITE}: {BOLD_GRAY}[{line},{character}]{BOLD_WHITE}: {message}{color.RESET}")
        exit(code)


class builddoc_warning(builddoc_base_error):
    """
    Represents a warning from BuildDoc. Basically a message that warns you of a potential error,
    or something small that's more of a harmless issue than an error.
    """

    def __init__(self, message: str) -> None:
        print(
            f"builddoc: {color.WARNING}warning{BOLD_WHITE}: {message}{color.RESET}")


class builddoc_unexpected_char_error(builddoc_base_error):
    def __init__(self, char: str, line: int, character: int, code: int = 2) -> None:
        print(
            f"builddoc: {color.ERROR}error{BOLD_WHITE}: {BOLD_GRAY}[{line},{character}]{BOLD_WHITE}: Unexpected `{char}`.{color.RESET}")
        exit(code)


class builddoc_syntax_error(builddoc_base_error):
    def __init__(self, syntax_message: str, bad_syntax: str, line: int, character: int, code: int = 4) -> None:
        print(
            f"builddoc: {color.ERROR}error{BOLD_WHITE}: {BOLD_GRAY}[{line},{character}]{BOLD_WHITE}: Bad syntax ({syntax_message}): `{bad_syntax}`.{color.RESET}")
        exit(code)


class builddoc_config_error(builddoc_base_error):
    def __init__(self, message: str, code: int = 1) -> None:
        print(
            f"builddoc-conf: {color.ERROR}error{BOLD_WHITE}: {BOLD_GRAY}: {message}{color.RESET}")
        exit(code)
