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


You will need to configure a local webserver as a proxy - see extra/piccolo_admin.
