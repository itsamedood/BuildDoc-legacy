from console.error import *
from sys import platform
import os
import json


class GlobalVars:
    """
    Class that reads and parses `.builddoc-global-vars.json`.
    """

    @staticmethod
    def check_for_global_vars_file() -> "str | None":
        if platform == "darwin" or platform == "linux" or platform == "linux2":  # MacOS or Linux.
            HOME = os.getenv("HOME")
            PATH = f"{HOME}/.builddoc/.builddoc-global-vars.json"

            try:
                for entry in os.scandir(f"{HOME}/.builddoc"):
                    if entry.is_file() and entry.name.lower() == ".builddoc-global-vars.json":
                        return PATH
                return None

            except:  # In theory, this should never happen.
                builddoc_warning("Directory '~/.builddoc' not found.")

        elif platform == "win32":  # Windows.
            pass

    @staticmethod
    def get_global_vars():
        PATH = GlobalVars.check_for_global_vars_file()

        if PATH is not None:
            with open(PATH, "r") as global_vars_file:
                global_vars: "dict[str, str]" = {}

                try:
                    data: "dict[str, dict[str, str]]" = json.load(
                        global_vars_file)

                    for obj in data:
                        if obj == "vars":
                            global_vars = data[obj]

                        else:
                            raise builddoc_config_error(
                                f"Invalid configuration: '{obj}'.")

                except:
                    builddoc_warning("Global vars file empty.")
                    return None

                finally:
                    global_vars_file.close()

        else:
            builddoc_warning("Global vars file not found.")
            return None

        return global_vars
