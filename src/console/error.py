from console.color import Color
from sys import exit

BOLD_WHITE = Color.ansi(1, 37)
BOLD_GRAY = Color.ansi(1, 39)


class builddoc_base_error(BaseException):
    """
    Base class for BuildDoc errors and such.
    """

    def __init__(self, message: str, code: int = 1) -> None:
        print(
            f"builddoc: {Color.ERROR}error{BOLD_WHITE}: {message}{Color.RESET}")
        exit(code)


class builddoc_error(builddoc_base_error):
    """
    Represents an error from BuildDoc, whether it be internal or caused by the user.
    """

    def __init__(self, message: str, line: int, character: int, code: int = 1) -> None:
        print(
            f"builddoc: {Color.ERROR}error{BOLD_WHITE}: {BOLD_GRAY}[{line},{character}]{BOLD_WHITE}: {message}{Color.RESET}")
        exit(code)


class builddoc_warning(builddoc_base_error):
    """
    Represents a warning from BuildDoc. Basically a message that warns you of a potential error,
    or something small that's more of a harmless issue than an error.
    """

    def __init__(self, message: str) -> None:
        print(
            f"builddoc: {Color.WARNING}warning{BOLD_WHITE}: {message}{Color.RESET}")


class builddoc_unexpected_char_error(builddoc_base_error):
    def __init__(self, char: str, line: int, character: int, code: int = 2) -> None:
        print(
            f"builddoc: {Color.ERROR}error{BOLD_WHITE}: {BOLD_GRAY}[{line},{character}]{BOLD_WHITE}: Unexpected `{char}`.{Color.RESET}")
        exit(code)


class builddoc_syntax_error(builddoc_base_error):
    def __init__(self, syntax_message: str, bad_syntax: str, line: int, character: int, code: int = 3) -> None:
        print(
            f"builddoc: {Color.ERROR}error{BOLD_WHITE}: {BOLD_GRAY}[{line},{character}]{BOLD_WHITE}: Bad syntax ({syntax_message}): `{bad_syntax}`.{Color.RESET}")
        exit(code)


class builddoc_command_error(builddoc_base_error):
    def __init__(self, task: str, command: str, code: int = 4) -> None:
        print(
            f"builddoc: {Color.ERROR}error{BOLD_WHITE}: {BOLD_GRAY}[{task}]{BOLD_WHITE}: Command failed: `{command}`.{Color.RESET}")
        exit(code)


class builddoc_config_error(builddoc_base_error):
    def __init__(self, message: str, code: int = 1) -> None:
        print(
            f"builddoc-conf: {Color.ERROR}error{BOLD_WHITE}: {BOLD_GRAY}: {message}{Color.RESET}")
        exit(code)
