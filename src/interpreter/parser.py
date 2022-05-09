from console.error import builddoc_syntax_error
from interpreter.tokens import *


class parser:
    """
    BuildDoc parser.
    """

    def parse(vars_dict: "dict[str, tuple[str, int]]", tasks_dict: "dict[str, list[tuple[str, int]]]"):
        """
        Parses variables and commands from dictionaries, provided by the lexer.
        """

        variable: str = ""
        single_quote: bool = False
        double_quote: bool = False
        reading_var: bool = False

        # Parsing variables.
        for var in vars_dict:
            value: str = vars_dict[var][0]
            line: int = vars_dict[var][1]

            if value.startswith(WHITESPACE) or value.startswith(TAB):
                raise builddoc_syntax_error(
                    "space/tab between `=` and value", f"{var}= {value}", line, len(var)+2)
            else:
                # Looping through every character in the value.
                for c in range(len(value)):
                    if c == 0:
                        if value[c] is SINGLE_QUOTE:
                            print("single q")
                            single_quote = True
                        elif value[c] is DOUBLE_QUOTE:
                            print("double q")
                            double_quote = True
                        else:
                            pass
                    else:
                        if value[c] is VARBL_OP:
                            print("variable to be used")
                            reading_var = True
                        else:
                            if reading_var:
                                if value[c] in LOWER_LETTER or value[c] in UPPER_LETTER:
                                    variable += value[c]
                                else:
                                    if not len(variable) > 0:
                                        raise builddoc_syntax_error(
                                            "no variable name given at `$` in value", value, line, c+1)
                                    print(variable)
                                    variable = ""

        if len(variable) > 0:
            print(variable)

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
                        # print(f"{cmd} @ {line}")
                        pass
