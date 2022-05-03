from interpreter.tokens import *
from console.error import *


# This took way too long, because I started off trying to read character by character, which caused like
# a million bugs, so then I tried it 2 MORE TIMES, before giving up and reading line by line, then for each line,
# THEN I read character by character.
class lexer:
    """
    Lexer class.
    """

    def tokenize(code: str) -> list:
        """
        "Tokenizes" `code` for the parser.

        Index `0` is the variables dictionary.

        Index `1` is the tasks dictionary.
        """

        # STRINGS #
        section: str = ""
        command: str = ""
        var_name: str = ""
        var_value: str = ""

        # BOOLEANS #
        reading_var_name: bool = True

        # DICTIONARIES #
        var_dict: "dict[str, tuple[str, int]]" = {}
        task_dict: "dict[str, list[str]]" = {}

        try:
            lines = code.split("\n")

            # Looping through every line.
            for line in range(len(lines)):
                # print(f"vars = {var_dict}")
                # print(f"tasks = {task_dict}")

                # line[0] was throwing an IndexError... ¯\_(ツ)_/¯
                if lines[line].startswith(COMMENT):
                    continue
                elif lines[line].startswith(L_BRACKET):  # Sections.
                    section = ""
                    chars: "list[str]" = [c for c in lines[line][1:]]

                    for c in range(len(chars)):
                        if chars[c] != R_BRACKET:
                            if chars[c] in LOWER_LETTER or chars[c] in UPPER_LETTER or chars[c] == PERIOD or chars[c] == UNDERSCORE:
                                section += chars[c]
                            else:
                                raise builddoc_unexpected_char_error(
                                    chars[c], line+1, c+1)
                        else:
                            # Checking if a section name was provided.
                            if len(section) > 0:
                                # print(section)
                                break
                            else:
                                raise builddoc_syntax_error(
                                    "Missing section name", "[]", line+1, c+1)
                elif lines[line].startswith(WHITESPACE) or lines[line].startswith(TAB) and section == ".VARS":
                    raise builddoc_syntax_error(
                        "line starts with whitespace or tab", " [...]", line+1, c+1)
                else:
                    chars: "list[str]" = [c for c in lines[line]]
                    c: int = 0

                    # Looping through the characters.
                    while c < len(chars):
                        # Reading variables.
                        # The parser will handle any syntax errors here.
                        if section == ".VARS":
                            if reading_var_name:
                                if chars[c] in LOWER_LETTER or chars[c] in UPPER_LETTER or chars[c] == UNDERSCORE or chars[c] == ASSIN_OP:
                                    if chars[c] == ASSIN_OP:
                                        reading_var_name = False
                                    else:
                                        var_name += chars[c]
                                else:
                                    raise builddoc_unexpected_char_error(
                                        chars[c], line+1, c+1)
                            else:
                                var_value += chars[c]

                        # Reading commands.
                        else:
                            command += chars[c]

                        c += 1  # End of loop.

                    if section == ".VARS":
                        # Set variable in dictionary, then reset variables used.
                        var_dict.__setitem__(var_name, (var_value, line+1))
                        var_name, var_value = "", ""
                        reading_var_name = True
                    else:
                        if section not in task_dict:
                            task_dict.__setitem__(section, [command])
                        else:
                            task_dict[section].append(command)

                        command = ""

        except KeyboardInterrupt:
            # This should never really happen, but just in case.
            raise builddoc_base_error("\nKeyboard interrupted.", 255)
        # except:
        #     raise builddoc_base_error("Internal error.", 500)  # lol.

        return [var_dict, task_dict]
