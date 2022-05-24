from console.error import builddoc_base_error, builddoc_error
from io import TextIOWrapper
from sys import argv
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from config.config import Config
import os


"""
This comment / complaint applies almost everywhere:
Although the parameters ("str | None") without quotation marks is valid syntax (str | None), but in certain cases,
it breaks everything for some reason.
Words cannot describe my confusion.
"""


class Main:
    """
    Starting point, where everything needed to initialize BuildDoc is stuffed into this class.
    """

    cwd = os.getcwd()

    def __init__(self) -> None:
        pass

    def check_for_builddoc(self) -> "str | None":
        """
        Checks to see if `./BuildDoc` exists, returning the path to it if it does. If it doesn't,
        `None` is returned.
        """

        for entry in os.scandir(self.cwd):
            if entry.is_file() and entry.name.lower() == "builddoc":
                return f"{self.cwd}/BuildDoc"
            else:
                continue
        return None

    def run(self, path: str, task: "str | None") -> None:
        """
        Maps, parses, and runs `task` in the BuildDoc.
        """

        try:
            builddoc: TextIOWrapper = open(path, "r")
            code: str = builddoc.read()

            # Read `.builddoc-conf.json`.
            Config.read_configs()

            # Lexer & Parser.
            dicts = Lexer.map(code)
            parsed_dicts = Parser.parse(dicts[0], dicts[1])
            parsed_vars = parsed_dicts[0]
            parsed_tasks = parsed_dicts[1]

        except KeyboardInterrupt:
            print("")
            raise builddoc_base_error("Keyboard interrupted.", 255)

        # except:
        #     raise builddoc_base_error("Internal error.")

        finally:
            builddoc.close()  # Always close an open file!


if __name__ == "__main__":
    MAIN: Main = Main()
    path: "str | None" = MAIN.check_for_builddoc()

    try:
        assert path is not None

        if len(argv) > 1:
            MAIN.run(path, argv[1])
        else:
            MAIN.run(path, None)
    except AssertionError:
        raise builddoc_error("No BuildDoc found.")
