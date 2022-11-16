Debugging
=========

Logging
-------

If Piccolo Admin encounters a ``500`` error, for example:

* The database is unavailable
* A table doesn't exist

Then Piccolo Admin will use Python's :meth:`exception logger <logging.Logger.exception>`
to log the exception. If running the app via uvicorn, you will then see the
exception traceback in the terminal.

Debug mode
----------

During development, you can run Piccolo Admin in debug mode.

.. code-block:: python

    app = create_admin(tables=[MyTable], debug=True)

When a ``500`` error is returned via the API, a stack trace is included.

This is useful if you want to inspect any ``500`` errors from the API in the
browser.

.. warning::

  DO NOT USE THIS IN PRODUCTION - the stack traces are for the developer's eyes
  only.
