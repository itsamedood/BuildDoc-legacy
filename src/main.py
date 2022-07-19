from config.global_vars import GlobalVars
from console.error import *
from sys import argv
from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.tokens import *
from console.color import Color
from enum import Enum
import sys
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
        if code > 0:
            raise builddoc_base_error(f"Exited with code {code}.", code)
        sys.exit(0)

    @staticmethod
    def run(path: str, task: "str | None") -> None:
        """
        Interprets the BuildDoc (determined by `path`), then runs every command in `task`.
        """

        exit_code = 1

        try:
            with open(path, "r") as builddoc:
                code = builddoc.read()

                if not len(code) > 0:
                    raise builddoc_base_error("BuildDoc is empty.")

                # Get global vars.
                global_vars = GlobalVars.get_global_vars()

                # Lexer & Parser.
                dicts = Lexer.map(code)

                parsed_vars = Parser.parse_values(dicts[0], global_vars)
                parsed_task = Parser.parse_task(task, dicts[1], parsed_vars)

                # Running the task.
                task_name = parsed_task[0]

                c = 0
                cmds = parsed_task[1][task_name]

                while c < len(parsed_task[1][task_name]):
                    if type(cmds[c]) is str:  # Regular command.
                        if cmds[c][0] is AND:  # Silenced.
                            ran_cmd = os.system(cmds[c][1:])

                            if ran_cmd > 0:
                                exit_code = ran_cmd
                                raise builddoc_command_error(
                                    task_name, cmds[c][1:], exit_code)

                        else:  # Not silenced.
                            print(cmds[c])
                            ran_cmd = os.system(cmds[c])

                            if ran_cmd > 0:
                                exit_code = ran_cmd
                                raise builddoc_command_error(
                                    task_name, cmds[c], exit_code)

                    else:  # Macro.
                        macro = cmds[c][0]
                        args = cmds[c][1].split(
                            ",") if len(cmds[c][1].split(",")) > 1 else cmds[c][1]
                        line: int = cmds[c][2]

                        actual_macro_line = f"%{macro}({args})"

                        if macro == "pass":
                            pass

                        elif macro == "goto":
                            Main.run(PATH, args)

                        elif macro == "warn":
                            if type(args) is str:
                                if args[0] is DOUBLE_QUOTE or args[0] is SINGLE_QUOTE:
                                    if args[0] == args[-1]:
                                        args = args[1:-1]

                                    else:
                                        raise builddoc_syntax_error(
                                            "non-matching quotes", f"({args})", line, len(actual_macro_line))

                                builddoc_warning(args)
                            else:
                                raise builddoc_syntax_error(
                                    f"expected 1 argument, got {len(args)}", actual_macro_line, line, len(actual_macro_line))

                        elif macro == "error":
                            if type(args) is str:
                                raise builddoc_syntax_error(
                                    f"expected 2 arguments, got 1", actual_macro_line, line, len(actual_macro_line))

                            if args[0][0] is DOUBLE_QUOTE or args[0][0] is SINGLE_QUOTE:
                                if args[0][0] == args[0][-1]:
                                    args[0] = args[0][1:-1]

                                else:
                                    raise builddoc_syntax_error(
                                        "non-matching quotes", f"({args})", line, len(actual_macro_line))

                            exit_code = int(args[1])
                            raise builddoc_base_error(args[0], exit_code)

                        else:
                            raise builddoc_error(
                                f"Unknown macro: `{macro}`.", line, len(macro))

                    c += 1  # 🏁

        except KeyboardInterrupt:
            print("")
            raise builddoc_base_error("Keyboard interrupted.", 255)

        except BaseException as BE:
            if len(BE.args) > 1:
                print(BE)
            Main.exit(exit_code)

        finally:
            return builddoc.close()  # Always close an open file!


if __name__ == "__main__":
    VERSION = "0.0.1"
    RELEASE_STAGE = [
        f"{Color.BLACK}Nightly{Color.RESET}",
        f"{Color.PURPLE}Alpha{Color.RESET}",
        f"{Color.BLUE}Beta{Color.RESET}",
        f"{Color.GREEN}Stable{Color.RESET}"
    ]

    PATH = Main.check_for_builddoc()

    try:
        assert PATH is not None

        # Checking for args.
        if len(argv) > 1:
            # Checking if the version flag was given. If so, print the version and exit. Otherwise, proceed.
            if argv[1] == "--version" or argv[1] == "-v":
                print(
                    f"{Color.BOLD}BuildDoc v{VERSION} [{RELEASE_STAGE[1]}]")
                Main.exit(0)

            Main.run(PATH, argv[1])

        else:
            Main.run(PATH, None)

    except AssertionError:
        raise builddoc_base_error("No BuildDoc found.")
