from os import getenv, popen
from console.error import *
from interpreter.tokens import *


class Parser:
    """
    BuildDoc parser.
    """

    @staticmethod
    def parse_line(line: str, line_num: "int | None", parsed_vars: "dict[str, tuple[str, int]]", line_is_cmd=False) -> str:
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
                            # `or chars[c] in NUMBER `.
                            if line[c] in LOWER_LETTER or line[c] in UPPER_LETTER or line[c] is UNDERSCORE:
                                variable += line[c]
                            else:
                                if not len(variable) > 0:
                                    raise builddoc_syntax_error(
                                        "no variable name given at `$` in value", line, line_num, c+1)

                                try:
                                    if line_is_cmd:
                                        line = line.replace(
                                            f"${variable}", parsed_vars[variable])
                                    else:
                                        line = line.replace(
                                            f"${variable}", parsed_vars[variable][0])
                                except KeyError:
                                    if line_num is not None:
                                        raise builddoc_error(
                                            f"Unknown variable: `{variable}`.", line_num, c+1)
                                    else:
                                        raise builddoc_base_error(
                                            f"Unknown global variable: `{variable}`.")

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
                                        "expected `{` to precede `?`", line, line_num, c+1)
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
                                        "closing `}` with no `{`", line, line_num, c+1)
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
                if line_is_cmd:
                    line = line.replace(
                        f"${variable}", parsed_vars[variable])
                else:
                    line = line.replace(
                        f"${variable}", parsed_vars[variable][0])

            except KeyError:
                if line_num is not None:
                    raise builddoc_error(
                        f"Unknown variable: `{variable}`.", line_num, len(variable))
                else:
                    raise builddoc_base_error(
                        f"Unknown global variable: `{variable}`.")

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
            raise builddoc_base_error(f"Shell command never closed: `{line}`.")

        # Checking if the line is a command and getting rid of the comment on the end (if any).
        if line_is_cmd:
            for c in range(len(line)):
                if line[c] is COMMENT:
                    if line[c-1] is WHITESPACE or line[c-1] is TAB:
                        line = line[0:c-1]
                        break
                    line = line[0:c]
                    break

        return line

    @staticmethod
    def parse_macro(macro: str, line: int) -> "tuple[str, str, int]":
        """
        Parses `macro`, returning the macro name and value / argument(s).
        """

        macro_name, macro_contents = "", ""
        macro_open = False

        for c in range(len(macro)):
            if macro[c] is MACRO_OP:
                continue

            elif macro[c] is L_PARENTH:
                macro_open = True

            elif macro[c] is R_PARENTH:
                if macro_open:
                    break
                else:
                    raise builddoc_syntax_error(
                        f"Unopened `)`.", macro, line, c+1)

            else:
                if macro_open:
                    if macro[c] in ALL_OPERATORS:
                        raise builddoc_syntax_error(
                            f"operator `{macro[c]}` in macro argument", macro, line, c+1)
                    macro_contents += macro[c]

                else:
                    macro_name += macro[c]

        if not macro_open:
            actual_macro_name = ""

            for c in macro:
                if c is WHITESPACE or c is TAB or c is COMMENT:
                    break
                else:
                    actual_macro_name += c

            raise builddoc_syntax_error(
                f"macro never opened", actual_macro_name, line, len(actual_macro_name))

        return (macro_name, macro_contents, line)

    @staticmethod
    def condition_is_true(logic_keyword: str, condition: str, line: int) -> bool:
        """
        Reads `condition`, returning `True` or `False`.
        """

        left_operand, right_operand = "", ""
        comma = False
        c = 0

        while c < len(condition):
            if comma:
                if condition[c] is COMMA:
                    raise builddoc_unexpected_char_error(
                        condition[c], line, c+1)

                right_operand += condition[c]

            else:
                if condition[c] is COMMA:
                    comma = True
                else:
                    left_operand += condition[c]

            c += 1  # 🏁

        if logic_keyword == "ifeq" or logic_keyword == "elifeq":
            return left_operand == right_operand

        elif logic_keyword == "ifneq" or logic_keyword == "elifneq":
            return not left_operand == right_operand

    @staticmethod
    def parse_values(vars_dict: "dict[str, tuple[str, int]]", global_vars: "dict[str, str]") -> "dict[str, tuple[str, int]]":
        """
        Parses all variable values (including global, which is parsed first).
        """

        parsed_vars_dict: dict[str, str] = {}

        # Global variables.
        for gvar in global_vars:
            gvalue = global_vars[gvar]
            parsed_gvalue = Parser.parse_line(
                gvalue, None, parsed_vars_dict, True)

            if len(parsed_gvalue) > 0:
                parsed_vars_dict[gvar] = parsed_gvalue

        # Local variables.
        for var in vars_dict:
            value = vars_dict[var][0]
            line = vars_dict[var][1]
            parsed_value = Parser.parse_line(value, line, vars_dict, False)

            if len(parsed_value) > 0:
                parsed_vars_dict[var] = parsed_value

        return parsed_vars_dict

    @staticmethod
    def parse_task(task: "str | None", tasks: "dict[str, list[tuple[str, int]]]", parsed_variables: "dict[str, tuple[str, int]]") -> "tuple[str | None, dict[str, list[str | tuple[str]]]]":
        """
        Parses all commands in `task`.
        """

        # Checking if a task was specified and if it exists. If it `None`, the 1st task is used.
        if task is not None:
            if task not in tasks:
                raise builddoc_base_error(f"Unknown task: `{task}`.")

        else:
            for t in tasks:
                if len(t) > 0:
                    task = t  # `task` is now the default task in the BuildDoc.
                    break

        parsed_task: "dict[str, list[str | tuple[str, str, int]]]" = {}
        #                      0       1        2          3        4       5
        # LOGIC_KEYWORDS = ["ifeq", "ifneq", "elifeq", "elifneq", "else", "fi"]
        # cmd_check, condition = "", ""
        # in_if, brace_open, condition_result, any_cond_true = False, False, False, False

        parsed_task[task] = []

        for cmdln in tasks[task]:
            cmd = cmdln[0]
            line = cmdln[1]
            # c = 0

            # Checking for a conditional keyword & condition (if any).
            # while c < len(cmd):
            #     if cmd[c] is WHITESPACE or cmd[c] is TAB:
            #         pass

            #     elif cmd[c] is LINEFEED:
            #         break

            #     elif cmd[c] is L_BRACE:
            #         if cmd_check not in LOGIC_KEYWORDS:
            #             pass

            #         elif (cmd_check is LOGIC_KEYWORDS[0] or cmd_check is LOGIC_KEYWORDS[1]) or ((cmd_check is LOGIC_KEYWORDS[4] or cmd_check is LOGIC_KEYWORDS[5])) and in_if:
            #             raise builddoc_unexpected_char_error(
            #                 cmd_check, line, c+1)

            #         elif cmd_check is LOGIC_KEYWORDS[0] or cmd_check is LOGIC_KEYWORDS[1]:
            #             in_if = True
            #         brace_open = True

            #     elif cmd[c] is R_BRACE:
            #         if len(condition) < 1:
            #             raise builddoc_syntax_error(
            #                 "no condition given", f"{cmd_check} {{}}", line, c+1)

            #         elif not brace_open:
            #             raise builddoc_syntax_error(
            #                 "unopened `}`", cmd, line, c+1)

            #         brace_open = False
            #         break

            #     else:
            #         if brace_open:
            #             condition += cmd[c]
            #         else:
            #             cmd_check += cmd[c]

            #     c += 1  # 🏁

            # Checking if the first word is a logical keyword that has a condition.
            # if cmd_check in LOGIC_KEYWORDS[:3] and len(condition) > 0:
            #     condition_result: bool | None = Parser.condition_is_true(cmd_check, Parser.parse_line(
            #         condition, line, parsed_variables, True), line)

            #     print(f"{condition} is {condition_result}")

            # Checking if the first word is a logical keyword that has no condition, which is `else` or `fi`.
            # elif cmd_check in LOGIC_KEYWORDS[4:5] and len(condition) < 1 and not any_cond_true:
            #     if cmd_check is LOGIC_KEYWORDS[4] and not any_cond_true:
            #         pass

            #     elif cmd_check is LOGIC_KEYWORDS[5]:
            #         pass

            # elif any_cond_true:
            #     pass

            # else:
            #     cmd_check = ""

            # Running the command or macro.
            if len(cmd) > 0:  # `and len(cmd_check) < 1:` should go before `:`.
                if cmd[0] is MACRO_OP:
                    parsed_task[task].append(
                        Parser.parse_macro(cmd, line))

                else:
                    parsed_task[task].append(Parser.parse_line(
                        cmd, line, parsed_variables, True))

        # `in_if` is returned to check if the last if statement was closed.
        return (task, parsed_task, True)  # Replace `True` with `in_if` later.
