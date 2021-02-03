API documentation
=================

During development it is useful to have API documentation, showing all of the
supported endpoints and parameters.

After logging in to the Piccolo admin, you can go to ``/api/docs`` to
see `Swagger docs <https://github.com/swagger-api/swagger-ui>`_, or
``/api/redoc`` to see `Redoc docs <https://github.com/Redocly/redoc>`_ for the
API.

.. image:: https://raw.githubusercontent.com/piccolo-orm/piccolo_admin/master/docs/images/redoc.png

.. hint:: Unfortunately, due to CSRF middleware, the interactive features of
 Swagger only work for GET requests.
