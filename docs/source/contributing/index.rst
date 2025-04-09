Contributing
============

The backend is just vanilla Python.

The front end is built using Vue.js. To make modifications, clone the repo, and
``cd`` into the ``admin_ui`` directory.

Install the npm dependencies:

.. code-block:: bash

    npm install

And then you can launch the admin as follows:

.. code-block:: bash

    npm run dev

It will auto refresh the UI as you make changes to the source files.

The UI needs an API to interact with - the easiest way to do this is to use the
demo app.

If you are developing on a local copy, you will first need to build
distribution files that the backend relies on.

``cd`` into the ``admin_ui`` directory and run the following:

.. code-block:: bash

    npm run build-only

Then start the API:

.. code-block:: bash

    admin_demo

    # Or alternatively
    python -m piccolo_admin.example.app

    # You can also populate lots of test data
    python -m piccolo_admin.example.app --inflate=10000

    # To find out all available options:
    python -m piccolo_admin.example.app --help

-------------------------------------------------------------------------------

Code style
----------

Python
~~~~~~

Piccolo uses `Black <https://black.readthedocs.io/en/stable/>`_  for
formatting, preferably with a max line length of 79, to keep it consistent
with `PEP8 <python.org/dev/peps/pep-0008/>`_ .

You can configure `VSCode <https://code.visualstudio.com/>`_ by modifying
``settings.json`` as follows:

.. code-block:: javascript

    {
        "python.linting.enabled": true,
        "python.formatting.provider": "black",
        "python.formatting.blackArgs": [
            "--line-length",
            "79"
        ],
        "editor.formatOnSave": true
    }

Type hints are used throughout the project.

Front end
~~~~~~~~~

We use VSCode for front end development, as it has the excellent Vetur
extension.

Add the following to your VSCode ``settings.json``:

.. code-block:: javascript

   {
        // Standalone LESS and Typescript files
        "prettier.semi": false,
        "prettier.singleQuote": false,
        "prettier.tabWidth": 4,
        "prettier.trailingComma": "none",

        // Vetur - handles Vue files
        "vetur.format.enable": true,
        "vetur.format.options.tabSize": 4,
        "vetur.format.options.useTabs": false,
        "vetur.format.defaultFormatterOptions": {
            "prettier": {
                "semi": false,
                "singleQuote": false,
                "trailingComma": "none",
            },
        },
    }

-------------------------------------------------------------------------------

Storybook
---------

The project uses `Storybook JS <https://storybook.js.org/>`_, which is a nice
tool for viewing UI components in isolation. To launch it:

.. code-block:: bash

    npm run storybook

.. note:: This was temporarily removed in v1, but we will try and add it back.

-------------------------------------------------------------------------------

Playwright
----------

Playwright is a tool for running end to end tests. It enables us to check that the
entire application is working as expected.

Run all tests
~~~~~~~~~~~~~

From within the ``root`` folder, use the following command to run all of
the Playwright tests with dev server in parallel:

.. code-block:: bash

    ./scripts/run-e2e-test.sh

-------------------------------------------------------------------------------

Translations
------------

The Piccolo Admin UI supports translations for several languages. If you
would like to contribute a new language, it would be very appreciated.

Look in ``piccolo_admin/translations/data.py``. Use one of the existing
translations as a foundation.

We have a script which checks if any translations are missing, which you can
use if you like:

.. code-block:: bash

    python scripts/get_translations.py validate
