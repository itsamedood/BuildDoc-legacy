from console.error import *
from sys import platform
import os
import json


class Config:
    """
    Class that reads and parses `.builddoc-conf.json`.
    """

    @staticmethod
    def check_for_config_file() -> "str | None":
        if platform == "darwin" or platform == "linux" or platform == "linux2":  # MacOS or Linux.
            USER = os.getenv("USER")
            PATH = f"/Users/{USER}/.builddoc/.builddoc-conf.json"

            try:
                for entry in os.scandir(f"/Users/{USER}/.builddoc"):
                    if entry.is_file() and entry.name.lower() == ".builddoc-conf.json":
                        return PATH
                    else:
                        return None
            except:
                builddoc_warning("Directory '~/.builddoc' not found.")

        # else:  # Windows.
        #     PATH: str = "C:\\.builddoc\\.builddoc-conf.json"

        #     try:
        #         for entry in os.scandir("C:\\.builddoc"):
        #             if entry.is_file() and entry.name.lower() == ".builddoc-conf.json":
        #                 return PATH
        #             else:
        #                 return None
        #     except:
        #         print("shit that doesn't exist")

    @staticmethod
    def read_configs():
        path = Config.check_for_config_file()
        VALID_CONFIGURATIONS: list[str] = ["vars"]

        if path is not None:
            conf_file = open(path)

            try:
                data: dict[str, dict[str, str]] = json.load(conf_file)

                for obj in data:
                    if obj in VALID_CONFIGURATIONS:
                        global_vars = data[obj]
                    else:
                        raise builddoc_config_error(
                            f"Invalid configuration: '{obj}'.")

            except:
                raise builddoc_base_error("Config file error.")
            finally:
                conf_file.close()
        else:
            if platform == "darwin" or platform == "linux" or platform == "linux2":  # MacOS or Linux.
                builddoc_warning(
                    "No '.builddoc-conf.json' found in '~/.builddoc'.")
            else:
                builddoc_warning(
                    "No 'C:\\.builddoc\\.builddoc-conf.json' found in 'C:\\.builddoc'.")

        return

    @staticmethod
    def parse_configs():
        pass
