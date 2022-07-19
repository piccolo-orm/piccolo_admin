"""
This extracts the translations required from the Vue code.
"""

import os
import re

import targ

ROOT_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "admin_ui/src"
)

REGEX = re.compile(r"\$t\(\"[A-Za-z0-9\s]+\"\)")


def get_translations():
    """
    Walk the directories, if files ends in Vue, open it ... use a regex to
    extract the string.
    """
    for root, _, files in os.walk(ROOT_FOLDER):
        for file in files:
            if file.endswith(".vue"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    contents = f.read()
                    matches = REGEX.findall(contents)
                    if matches:
                        print("MATCHED")
                        print(matches)
                    else:
                        print("No matches")


def main():
    cli = targ.CLI(description="Get translation strings")
    cli.register(get_translations)
    cli.run(solo=True)


if __name__ == "__main__":
    main()
