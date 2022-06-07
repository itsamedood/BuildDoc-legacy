from os import getenv, popen
from console.error import *
from interpreter.tokens import *


# MUCH more organized now!
class Parser:
    """
    BuildDoc parser.
    """

    @staticmethod
    def parse_line(line: str, line_num: int, parsed_vars: "dict[str, tuple[str, int]]") -> str:
        """
        Parses any and all variables on `line`.
        """

        # STRINGS #
        variable = ""
        env_variable = ""
        shell_variable = ""

        # BOOLEANS #
        reading_var = False
        reading_env_var = False
        reading_shell_var = False
        shell_var_open = False

        for c in range(len(line)):
            if len(line) > 0:
                try:
                    if line[c] is VARBL_OP:
                        reading_var = True
                    elif line[c] is ENVVR_OP:
                        reading_env_var = True
                    elif line[c] is SHELL_OP:
                        reading_shell_var = True

                    else:
                        if reading_var:
                            if line[c] in LOWER_LETTER or line[c] in UPPER_LETTER or line[c] is PERIOD or line[c] is UNDERSCORE:
                                variable += line[c]
                            else:
                                if not len(variable) > 0:
                                    raise builddoc_syntax_error(
                                        "no variable name given at `$` in value", line, line_num, c+1)

                                try:
                                    line = line.replace(
                                        f"${variable}", parsed_vars[variable][0])
                                except KeyError:
                                    raise builddoc_error(
                                        f"Unknown variable: `{variable}`.", line_num, c+1)

                                variable = ""
                                reading_var = False

                        elif reading_env_var:
                            if line[c] in LOWER_LETTER or line[c] in UPPER_LETTER or line[c] is UNDERSCORE:
                                env_variable += line[c]
                            else:
                                if not len(env_variable) > 0:
                                    raise builddoc_syntax_error(
                                        "no env variable name given at `@` in value", line, line_num, c+1)

                                try:
                                    line = line.replace(
                                        f"@{env_variable}", getenv(env_variable))
                                except KeyError:
                                    raise builddoc_error(
                                        f"Unknown env variable: `{env_variable}`.", line_num, c+1)

                                env_variable = ""
                                reading_env_var = False

                        elif reading_shell_var:
                            if line[c] is L_BRACE:
                                if line[c-1] is SHELL_OP:
                                    shell_var_open = True
                                else:
                                    raise builddoc_syntax_error(
                                        "expected '{' to precede '?'", line, line_num, c+1)
                            elif line[c] is R_BRACE:
                                if shell_var_open:
                                    if len(shell_variable) > 0:
                                        try:
                                            output = popen(
                                                shell_variable).read()

                                            if output[-1] is LINEFEED:
                                                output = output[0:-1]

                                            line = line.replace(
                                                f"?{L_BRACE}{shell_variable}{R_BRACE}", output)

                                            shell_variable = ""
                                            shell_var_open, reading_shell_var = False, False
                                        except:
                                            raise builddoc_error(
                                                f"Failed to execute shell command: {L_BRACE}{shell_variable}{R_BRACE}", line_num, c+1)
                                    else:
                                        raise builddoc_syntax_error(
                                            "no shell command given at `?{` in value", line, line_num, c+1)
                                else:
                                    raise builddoc_syntax_error(
                                        "closing '}' with no '{'", line, line_num, c+1)
                            else:
                                shell_variable += line[c]
                except IndexError:  # Absolutely love Python sometimes...
                    pass

        # Fallbacks for parsing variables.
        # If the value does NOT end with a punctuation mark, then it breaks.
        # These if-statements counter that behavior.

        # Regular variables.
        if len(variable) > 0:
            try:
                line = line.replace(
                    f"${variable}", parsed_vars[variable][0])
            except KeyError:
                raise builddoc_error(
                    f"Unknown variable: `{variable}`.", line_num, len(variable))

        # Env variables.
        if len(env_variable) > 0:
            try:
                line = line.replace(
                    f"@{env_variable}", getenv(env_variable))
            except KeyError:
                raise builddoc_error(
                    f"Unknown env variable: `{env_variable}`.", line_num, len(env_variable))

        # Shell commands.
        # This isn't so much a fallback as it is a syntax error catcher.
        if len(shell_variable) > 0:
            raise builddoc_base_error(f"Shell command never closed: '{line}'.")

        return line

    @staticmethod
    def parse_values(vars_dict: "dict[str, tuple[str, int]]") -> "dict[str, tuple[str, int]]":
        """
        Parses all variable values.
        """

        parsed_vars_dict: dict[str, str] = {}

        # Parsing variables.
        for var in vars_dict:
            value = vars_dict[var][0]
            line = vars_dict[var][1]
            parsed_value = Parser.parse_line(value, line, vars_dict)

            if parsed_value is not value and len(parsed_value) > 0:
                parsed_vars_dict[var] = parsed_value

        return parsed_vars_dict

    # @staticmethod
    # def parse_tasks(tasks_dict: "dict[str, list[tuple[str, int]]]") -> "dict[str, list[tuple[str, int]]]":
    #     """
    #     Parses all commands in each task.
    #     """

    #     # STRINGS #
    #     command = ""
    #     macro_name = ""
    #     macro_contents = ""
    #     condition = ""

    #     # BOOLEANS #
    #     reading_macro = False
    #     done_with_macro_name = False
    #     silenced = False

    #     # OTHER #
    #     parsed_tasks_dict: dict[str, list[str]] = {}

    #     # Parsing tasks.
    #     for task in tasks_dict:
    #         if len(task) < 1:
    #             continue
    #         else:
    #             tuples: list[tuple[str, int]] = [c for c in tasks_dict[task]]

    #             for tup in tuples:
    #                 cmd = tup[0]
    #                 line = tup[1]

    #                 if len(cmd) < 1:
    #                     continue

    #     return parsed_tasks_dict

    # @staticmethod
    # def verify_syntax_of_macro(macro: str, line: int) -> None:
    #     """
    #     Ensures that nothing follows the closing parenthesis in a macro call, as well as checking that the call is
    #     syntatically correct.
    #     """

    #     c = 0
    #     paren_open = False
    #     paren_good = False

    #     while c < len(macro):
    #         if macro[c] is L_PARENTH:
    #             paren_open = True
    #         elif macro[c] is R_PARENTH:
    #             if paren_open:
    #                 paren_good, paren_open = True, False
    #             else:
    #                 raise builddoc_syntax_error(
    #                     "invalid macro syntax", macro, line, c+1)

    #         else:
    #             if paren_open:
    #                 pass
    #             elif paren_good:
    #                 if macro[c] is WHITESPACE or macro[c] is TAB:
    #                     pass
    #                 elif macro[c] is COMMENT:
    #                     break
    #                 else:
    #                     raise builddoc_unexpected_char_error(
    #                         macro[c], line, c+1)
    #             else:
    #                 pass

    #         c += 1  # 🏁

    # @staticmethod
    # def read_macro(macro: str, value: str, line: int) -> None:
    #     """
    #     Reads and executes the given macro.
    #     """

    #     if macro == "goto":
    #         print(f"go over to '{value}'.")
    #     else:
    #         raise builddoc_error(
    #             f"Invalid macro: '{macro}'.", line, len(macro))
