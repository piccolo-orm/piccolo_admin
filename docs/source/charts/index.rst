.. _Charts:

Charts
======

Piccolo Admin can display different types of charts based on your
data. Five chart types are supported:

* ``Pie``
* ``Line``
* ``Column``
* ``Bar``
* ``Area``

``ChartConfig``
---------------

To configure charts use :class:`ChartConfig <piccolo_admin.endpoints.ChartConfig>`.

Full example
------------

Here's a full example of charts usage, using FastAPI:

.. literalinclude:: ./examples/app.py

Piccolo Admin will then show a chart in the UI.

.. image:: ./images/charts_sidebar.png

.. image:: ./images/chart.png

-------------------------------------------------------------------------------

Source
------

.. currentmodule:: piccolo_admin.endpoints

.. autoclass:: ChartConfig
.. autoclass:: ChartDataSource
