Installation
============

Python 3.8 or above is required.

Install ``piccolo_admin``, ideally inside a `virtualenv <https://docs.python-guide.org/dev/virtualenvs/>`_.

.. code-block:: bash

    pip install piccolo_admin

-------------------------------------------------------------------------------

Local demo
----------

To run a demo locally:

.. code-block:: bash

    admin_demo

And then just launch `<localhost:8000>`_ in your browser. Login using ``username: piccolo, password: piccolo123``.

To see what happens behind the scenes, see ``piccolo_admin/example/app.py``.

In a few lines of code we are able to:

* Define our tables
* Setup a database
* Create a REST API
* Setup a web server and admin interface

Next we'll look at integrating the Piccolo admin properly into your own project.
