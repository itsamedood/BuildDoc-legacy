from os import getenv, popen
from console.error import builddoc_base_error, builddoc_error, builddoc_syntax_error
from interpreter.tokens import *


class Parser:
    """
    BuildDoc parser.
    """

    def parse(vars_dict: "dict[str, tuple[str, int]]", tasks_dict: "dict[str, list[tuple[str, int]]]"):
        """
        Parses variables and commands from dictionaries, provided by the lexer.
        """

        # STRINGS #
        variable: str = ""
        env_variable: str = ""
        shell_variable: str = ""

        # BOOLEANS #
        reading_var: bool = False
        reading_env_var: bool = False
        reading_shell_var: bool = False
        shell_var_open: bool = False

        parsed_vars_dict: "dict[str, str]" = {}
        parsed_tasks_dict: "dict[str, list[str]]" = {}

        # Parsing variables.
        for var in vars_dict:
            value: str = vars_dict[var][0]
            line: int = vars_dict[var][1]

            if len(var) > 0:
                parsed_vars_dict[var] = value

            if value.startswith(WHITESPACE) or value.startswith(TAB):
                raise builddoc_syntax_error(
                    "space/tab between `=` and value", f"{var}= {value}", line, len(var)+2)
            else:
                # Looping through every character in the value.
                for c in range(len(value)):
                    # Operators.
                    if value[c] is VARBL_OP:
                        reading_var = True
                    elif value[c] is ENVVR_OP:
                        reading_env_var = True
                    elif value[c] is SHELL_OP:
                        reading_shell_var = True

                    # Actual parsing.
                    else:
                        if reading_var:
                            if value[c] in LOWER_LETTER or value[c] in UPPER_LETTER or value[c] is UNDERSCORE:
                                variable += value[c]
                            else:
                                if not len(variable) > 0:
                                    raise builddoc_syntax_error(
                                        "no variable name given at `$` in value", value, line, c+1)

                                try:
                                    parsed_vars_dict[var] = parsed_vars_dict[var].replace(
                                        f"${variable}", vars_dict[variable][0])
                                except KeyError:
                                    raise builddoc_error(
                                        f"Unknown variable: '{variable}'.", line, c+1)
                                variable = ""
                                reading_var = False

                        elif reading_env_var:
                            if value[c] in LOWER_LETTER or value[c] in UPPER_LETTER or value[c] is UNDERSCORE:
                                env_variable += value[c]
                            else:
                                if not len(env_variable) > 0:
                                    raise builddoc_syntax_error(
                                        "no env variable name given at `@` in value", value, line, c+1)

                                try:
                                    parsed_vars_dict[var] = parsed_vars_dict[var].replace(
                                        f"@{env_variable}", getenv(env_variable))
                                except KeyError:
                                    raise builddoc_error(
                                        f"Unknown env variable: '{env_variable}'.", line, c+1)
                                env_variable = ""
                                reading_env_var = False

                        elif reading_shell_var:
                            if value[c] is L_BRACE:
                                if value[c-1] is SHELL_OP:
                                    shell_var_open = True
                                else:
                                    raise builddoc_syntax_error(
                                        "expected '{' to precede '?'", value, line, c+1)

                            elif value[c] is R_BRACE:
                                if shell_var_open:
                                    if len(shell_variable) > 0:
                                        try:
                                            output: str = popen(
                                                shell_variable).read()

                                            if output[-1] is LINEFEED:
                                                output = output[0:-1]

                                            parsed_vars_dict[var] = parsed_vars_dict[var].replace(
                                                f"?{L_BRACE}{shell_variable}{R_BRACE}", output)
                                            shell_variable = ""
                                            shell_var_open, reading_shell_var = False, False

                                        except:
                                            raise builddoc_error(
                                                f"Failed to execute shell command: {L_BRACE}{shell_variable}{R_BRACE}", line, c+1)

                                    else:
                                        raise builddoc_syntax_error(
                                            "no shell command given at `?{` in value", value, line, c+1)

                                else:
                                    raise builddoc_syntax_error(
                                        "closing '}' with no '{'", value, line, c+1)

                            else:
                                shell_variable += value[c]

            # Fallbacks for parsing variables.
            # If the value does NOT end with a punctuation, then it breaks.
            # These if-statements counter that behavior.

            # Regular variables.
            if len(variable) > 0:
                try:
                    parsed_vars_dict[var] = value.replace(
                        f"${variable}", vars_dict[variable][0])
                except KeyError:
                    raise builddoc_error(
                        f"Unknown variable: '{variable}'.", line, c+1)
                variable = ""
                reading_var = False

            # Env variables.
            if len(env_variable) > 0:
                try:
                    parsed_vars_dict[var] = value.replace(
                        f"@{env_variable}", getenv(env_variable))
                except KeyError:
                    raise builddoc_error(
                        f"Unknown env variable: '{env_variable}'.", line, c+1)
                env_variable = ""
                reading_env_var = False

            # Shell commands.
            # This isn't a fallback, it's more of a syntax error catcher.
            if len(shell_variable) > 0:
                raise builddoc_base_error(
                    f"Shell command never closed: '{value}'.")

        # print(f"PARSED VARS: {parsed_vars_dict}")

        # Parsing tasks.
        for task in tasks_dict:
            if len(task) < 1:
                continue
            else:
                commands: list[tuple[str, int]] = [c for c in tasks_dict[task]]

                for tup in commands:
                    cmd = tup[0]
                    line = tup[1]

                    if len(cmd) < 1:
                        continue
                    else:
                        print(f"{cmd} @ {line}")
                        pass

        print(f"PARSED TASKS: {parsed_tasks_dict}")
