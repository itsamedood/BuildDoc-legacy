from console.color import color
from sys import exit

BOLD_WHITE = color.ansi(1, 37)


class builddoc_error(BaseException):
    """
    Represents an error from BuildDoc, whether it be internal or caused by the user.
    """

    def __init__(self, message: str, code: int = 1) -> None:
        print(
            f"builddoc: {color.ERROR}error{BOLD_WHITE}: {message}{color.RESET}")
        exit(code)


class builddoc_warning(builddoc_error):
    """
    Represents a warning from BuildDoc. Basically a message that warns you of a potential error,
    or something small that's more of a harmless issue than an error.
    """

    def __init__(self, message: str) -> None:
        print(
            f"builddoc: {color.WARNING}warning{BOLD_WHITE}: {message}{color.RESET}")
