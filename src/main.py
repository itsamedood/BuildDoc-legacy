from console.error import builddoc_base_error, builddoc_error
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

    def check_for_builddoc() -> "str | None":
        """
        Checks to see if `./BuildDoc` exists, returning the path to it if it does. If it doesn't,
        `None` is returned.
        """

        cwd = os.getcwd()

        for entry in os.scandir(cwd):
            if entry.is_file() and entry.name.lower() == "builddoc":
                return f"{cwd}/BuildDoc"
            else:
                continue

        return None

    def run(path: str, task: "str | None") -> None:
        """
        Maps, parses, and runs `task` in the BuildDoc.
        """

        try:
            builddoc = open(path, "r")
            code = builddoc.read()

            # Read `.builddoc-conf.json`.
            # Config.read_configs()

            # Lexer & Parser.
            dicts = Lexer.map(code)
            parsed_vars = Parser.parse_values(dicts[0])
            # parsed_tasks = Parser.parse_tasks(dicts[1])

            print(parsed_vars)
        except KeyboardInterrupt:
            print("")
            raise builddoc_base_error("Keyboard interrupted.", 255)

        # except:
        #     raise builddoc_base_error("Internal error.")

        finally:
            builddoc.close()  # Always close an open file!


if __name__ == "__main__":
    PATH = Main.check_for_builddoc()

    try:
        assert PATH is not None

        if len(argv) > 1:
            Main.run(PATH, argv[1])
        else:
            Main.run(PATH, None)

    except AssertionError:
        raise builddoc_error("No BuildDoc found.")
