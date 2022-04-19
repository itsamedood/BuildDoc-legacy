from console.error import builddoc_error
import os


def check_for_builddoc():
    """
    Checks to see if `./BuildDoc` exists, returning the path to it if it does. If it doesn't,
    `None` is returned.
    """

    cwd = os.getcwd()

    try:
        for entry in os.scandir(cwd):
            if entry.is_file() and entry.name.lower() == "builddoc":
                return f"{cwd}/BuildDoc"
            else:
                continue
        return None
    except:
        raise builddoc_error("Internal error (unknown).")  # Just in case.


if __name__ == "__main__":
    path: "str | None" = check_for_builddoc()

    if path is not None:
        print(":D")
    else:
        raise builddoc_error("No BuildDoc found.")
