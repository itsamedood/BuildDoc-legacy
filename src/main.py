from console.error import builddoc_base_error, builddoc_command_error, builddoc_error
from sys import argv
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.tokens import AND
# from config.config import Config
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

    @staticmethod
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

    @staticmethod
    def exit(code=1) -> None:
        """
        Exits the program with the given code.
        """

        raise builddoc_base_error(f"Exited with code {code}.", code)

    @staticmethod
    def run(path: str, task: "str | None") -> None:
        """
        Interprets the BuildDoc (determined by `path`), then running every command in `task`.
        """

        exit_code = 1

        try:
            builddoc = open(path, "r")
            code = builddoc.read()

            # Read `.builddoc-conf.json`.
            # Config.read_configs()

            # Lexer & Parser.
            dicts = Lexer.map(code)

            parsed_vars = Parser.parse_values(dicts[0])
            parsed_task = Parser.parse_task(task, dicts[1], parsed_vars)

            # Running the task.
            task_name = parsed_task[0]

            for cmd in parsed_task[1][task_name]:
                if type(cmd) is str:  # Regular command.
                    if cmd[0] is AND:  # Silenced.
                        ran_cmd = os.system(cmd[1:])

                        if ran_cmd > 0:
                            exit_code = ran_cmd
                            raise builddoc_command_error(task_name, cmd[1:])
                    else:
                        print(cmd)
                        ran_cmd = os.system(cmd)

                        if ran_cmd > 0:
                            exit_code = ran_cmd
                            raise builddoc_command_error(task_name, cmd)

                else:  # Macro.
                    pass

        except KeyboardInterrupt:
            print("")
            raise builddoc_base_error("Keyboard interrupted.", 255)

        except:
            Main.exit(exit_code)

        finally:
            return builddoc.close()  # Always close an open file!


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
