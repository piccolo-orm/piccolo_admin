.. _HelpText:

Help Text
=========

Sometimes you will want to provide hints to your users about what the form
fields mean.

Using this table as an example:

.. code-block:: python

    from piccolo.table import Table
    from piccolo.columns import Varchar, Numeric


    class Movie(Table):
        name = Varchar(length=300)
        box_office = Numeric(digits=(5, 1))


It isn't immediately clear what ``box_office`` means. We can add a
``help_text`` attribute to the column:

.. code-block:: python

    from piccolo.table import Table
    from piccolo.columns import Varchar, Numeric


    class Movie(Table):
        name = Varchar(length=300)
        box_office = Numeric(digits=(5, 1), help_text="In millions of US dollars.")


Piccolo Admin will then show a tooltip next to this field.
