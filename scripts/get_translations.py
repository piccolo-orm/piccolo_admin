"""
This extracts the translations required from the Vue code.
"""

import os
import re
import sys

import targ

VUE_ROOT_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "admin_ui/src"
)

REGEX = re.compile(r"\$t\(\"[^\"]+\"")


def get_phrases():
    """
    Analyses the Vue files, and extracts any required translations.

    A translation within a Vue file looks like $t("A translation").

    """
    output = set()
    for root, _, files in os.walk(VUE_ROOT_FOLDER):
        for file in files:
            if file.endswith(".vue"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    contents = f.read()
                    matches = REGEX.findall(contents)
                    for match in matches:
                        output.add(match.lstrip('$t("').rstrip('"'))

    return output


def _print():
    """
    Just prints out the translations.
    """

    print("\n".join(sorted([i for i in get_phrases()])))


def validate():
    """
    Inspects the translations and prints out phrases are missing.
    """
    path = os.path.dirname(os.path.dirname(__file__))

    if path not in sys.path:
        sys.path.insert(0, path)

    from piccolo_admin.translations.data import TRANSLATIONS, VALIDATE_IGNORE

    phrases = get_phrases()

    success = True

    for translation in TRANSLATIONS:
        existing_keys = set(translation.translations.keys()) - set(
            VALIDATE_IGNORE
        )

        print(f"{translation.language_name}")

        print("\nMissing keys:\n")
        missing_keys = phrases - existing_keys
        if missing_keys:
            print("{")
            print(
                "\n".join(
                    f'    "{key}": "{key}",' for key in sorted(missing_keys)
                )
            )
            print("}")
            success = False
        else:
            print("None")

        print("\nSurplus keys:\n")
        surplus_keys = existing_keys - phrases
        if surplus_keys:
            print("\n".join(sorted(surplus_keys)))
            success = False
        else:
            print("None")

        print("\n------------\n")

    if not success:
        sys.exit("Some translations are out of date.")
    else:
        print("Everything is good!")


def main():
    """
    To validate the translation file:

        python get_translations validate

    To print out the translations:

        python get_translations print

    """
    cli = targ.CLI(description="Get translation strings")
    cli.register(_print, command_name="print")
    cli.register(validate)

    cli.run()


if __name__ == "__main__":
    main()
