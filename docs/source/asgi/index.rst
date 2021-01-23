ASGI
====

Since the admin is an `ASGI app <https://piccolo-orm.com/blog/introduction-to-asgi/>`_, you can either run it standalone like in the demo, or integrate it with a larger ASGI app.

.. hint:: Piccolo can help you `create a new ASGI app <https://piccolo-orm.readthedocs.io/en/latest/piccolo/asgi/index.html>`_ - using ``piccolo asgi new``.

For example, using Starlette routes:

.. code-block:: python

    from piccolo_admin.endpoints import create_admin
    from starlette.routing import Router, Route
    import uvicorn

    from my_project.tables import Director, Movie


    # The `allowed_hosts` argument is required when running under HTTPS. It's used
    # for additional CSRF defence.
    admin = create_admin([Director, Movie], allowed_hosts=['my_site.com'])


    router = Router([
        Route(path="/", endpoint=Hello),
        Mount(path="/admin/", app=admin),
    ])


    if __name__ == '__main__':
        uvicorn.run(router)

FastAPI example
---------------

Here's a complete example of a FastAPI app using Piccolo admin.

.. code-block:: python

    # app.py
    from fastapi import FastAPI
    from piccolo.engine import engine_finder
    from piccolo_admin.endpoints import create_admin
    from starlette.routing import Mount
    from my_project.tables import Director, Movie

    app = FastAPI(
        routes=[
            Mount(
                "/admin/",
                create_admin(
                    tables=[Director, Movie],
                    # Specify a different site name in the
                    # admin UI (default Piccolo Admin)
                    site_name = "Mysite Admin",
                    # Required when running under HTTPS:
                    # allowed_hosts=['my_site.com']
                ),
            ),
        ],
    )

    @app.on_event("startup")
    async def open_database_connection_pool():
        engine = engine_finder()
        await engine.start_connnection_pool()


    @app.on_event("shutdown")
    async def close_database_connection_pool():
        engine = engine_finder()
        await engine.close_connnection_pool()

To run ``app.py`` use:

.. code-block:: bash

    uvicorn app:app --port 8000 --host 0.0.0.0

Now you can go to `<localhost:8000/admin>`_ and log in as an admin user
(see :ref:`Authentication` for how to create users).

Source
------

.. currentmodule:: piccolo_admin.endpoints

.. autoclass:: create_admin
