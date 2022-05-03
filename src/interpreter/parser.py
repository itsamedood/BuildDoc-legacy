from console.error import builddoc_syntax_error
from interpreter.tokens import *


class parser:
    """
    BuildDoc parser.
    """

    def parse(vars_dict: "dict[str, tuple[str, int]]", tasks_dict: "dict[str, list[str]]"):
        # Parsing variables.
        for var in vars_dict:
            value = vars_dict[var][0]
            line = vars_dict[var][1]

            if value.startswith(WHITESPACE) or value.startswith(TAB):
                raise builddoc_syntax_error(
                    "space/tab between `=` and value", f"{var}= {value}", line, len(var)+2)
            else:
                pass

        # Parsing tasks.
        for task in tasks_dict:
            pass
