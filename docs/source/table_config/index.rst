TableConfig
===========

When using ``create_admin``, you can pass in normal ``Table`` classes:

.. code-block:: python

    from piccolo_admin.endpoints import create_admin

    create_admin([Director, Movie])

Alternatively, you can pass in ``TableConfig`` instances (or mix and match
them).

By passing in a ``TableConfig`` you have extra control over how the UI behaves
for that table. This is particularly useful when you have a ``Table`` with lots
of columns.

In the future, ``TableConfig`` will be extended to allow finer grained control
over the UI.

-------------------------------------------------------------------------------

visible_columns
---------------

We can set which columns are visible in the list view:

.. code-block:: python

    from piccolo_admin.endpoints import TableConfig

    movie_config = TableConfig(Movie, visible_columns=[Movie.id, Movie.name])

    create_admin([Director, movie_config])

Here is the UI when just passing in a ``Table``:

.. image:: ./images/without_visible_columns.jpg

Here is the UI when just passing in a ``TableConfig`` instance instead (fewer
columns are visible):

.. image:: ./images/with_visible_columns.jpg

-------------------------------------------------------------------------------

visible_filters
---------------

We can set which columns are visible in the filter sidebar:

.. code-block:: python

    from piccolo_admin.endpoints import TableConfig

    movie_config = TableConfig(
        Movie,
        visible_filters=[
            Movie.name, Movie.rating, Movie.director,
        ]
    )

    create_admin([Director, movie_config])

Here is the UI when just passing in a ``Table``:

.. image:: ./images/without_visible_filters.jpg

Here is the UI when just passing in a ``TableConfig`` instance instead (fewer
filters are visible in the sidebar):

.. image:: ./images/with_visible_filters.jpg

-------------------------------------------------------------------------------

rich_text_columns
-----------------

We can specify which ``Text`` columns will use a rich text editor.

.. code-block:: python

    from piccolo_admin.endpoints import TableConfig

    movie_config = TableConfig(
        Movie,
        rich_text_columns=[
            Movie.description
        ]
    )

    create_admin([Director, movie_config])

This allows the user to add hyperlinks, and basic formatting to their content,
without having to write HTML.

.. image:: ./images/rich_text_columns.jpg

-------------------------------------------------------------------------------

hooks
-----

Can be used to run custom logic when a row is created, modified, or deleted.

.. code-block:: python

    from piccolo_admin.endpoints import TableConfig
    from piccolo_api.crud.hooks import Hook, HookType


    async def my_save_hook(row: Movie):
        # Insert custom logic here
        return row


    movie_config = TableConfig(
        Movie,
        hooks=[
            Hook(hook_type=HookType.pre_save, callable=my_save_hook)
        ]
    )

    create_admin([Director, movie_config])

To learn more about hooks, see the :class:`Hook <piccolo_api.crud.hooks.Hook>`
docs in Piccolo API.

-------------------------------------------------------------------------------

Source
------

.. currentmodule:: piccolo_admin.endpoints

.. autoclass:: TableConfig
