Contributing
============

The backend is just vanilla Python.

The front end is built using Vue.js. To make modifications, clone the repo, and cd into the `admin_ui` directory.

Install the npm dependencies:

.. code-block:: bash

    npm install


And then you can launch the admin as follows:

.. code-block:: bash

    npm run serve


It will auto refresh the UI as you make changes to the source files.

The UI needs an API to interact with - the easiest way to do this is to use the demo app.

.. code-block:: bash

    admin_demo

    # Or alternatively
    python -m piccolo_admin.example

    # You can also populate lots of test data
    python -m piccolo_admin.example --inflate=10000

    # To find out all available options:
    python -m piccolo_admin.example --help


You will need to configure a local webserver as a proxy - see extra/piccolo_admin.


Storybook
---------

The project uses `Storybook JS <https://storybook.js.org/>`_, which is a nice tool
for viewing UI components in isolation. To launch it:

.. code-block:: bash

    npm run storybook


Cypress
-------

Cypress is a tool for running end to end tests. It enables us to check that the
entire application is working as expected.

Before launching it, make sure that the Piccolo Admin front end code and
backend code are running (see above).

Then launch Cypress as follows:

.. code-block:: bash

    npm run cypress:open


This will launch the Cypress app, which is basically a wrapper around Chrome,
from which you can start the automated tests.
