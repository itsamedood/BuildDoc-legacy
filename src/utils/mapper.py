class mapper:
    """
    Class for mapping variables and tasks.
    """

    @staticmethod
    def map_variables(code: str) -> "dict[str, str]":
        """
        Maps variables to their values.
        """

        lines = code.split("\n")
        for line in lines:
            print(line)

    @staticmethod
    def map_task(code: str, task: "str | None") -> "dict[str, list[str]]":
        """
        Maps `task` to it's commands.

        If `task` doesn't exist, an error is raised.
        """

        if task is not None:
            print(task)
        else:
            print(None)
