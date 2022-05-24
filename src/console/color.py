class Color:
    """
    Class for printing colored text, using ANSI codes.
    """

    # Normal.
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"
    GRAY = "\033[0;38m"

    # Style.
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    CROSSED = "\033[9m"
    UNDERLINE = "\033[4m"

    # Special.
    ERROR = "\033[1;31m"  # Bold & red.
    WARNING = "\033[1;33m"  # Bold & yellow.
    NOTE = "\033[1;38m"  # Bold & gray.
    RESET = "\033[0;0m"  # Un-does any changes.

    @staticmethod
    def ansi(style: int, color: int) -> str:
        """
        Creates a color from ANSI code.

        ```py
        bold_red = Color.ansi(1, 31)  # "\033[1;31m" = RED.
        ```
        """

        return f"\033[{style};{color}m"
