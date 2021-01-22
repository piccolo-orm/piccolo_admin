Authentication
==============

Session table
-------------

Piccolo admin uses `session auth <https://piccolo-api.readthedocs.io/en/latest/session_auth/index.html>`_, 
which requires a ``Session`` database table.

Add ``piccolo_admin.piccolo_app`` to the APP_REGISTRY in your ``piccolo_conf.py``
project file, then run migrations:

.. code-block:: bash

    piccolo migrations forwards session_auth

To learn more about the Piccolo project files, check out the 
Piccolo ORM `docs <https://piccolo-orm.readthedocs.io/en/latest/piccolo/projects_and_apps/piccolo_apps.html>`_.


Create user
-----------

``BaseUser`` is a ``Table`` you can use to store and authenticate your users. 
You need this table to be able to create user with admin privileges. 
``BaseUser`` is shipped out of the box with Piccolo and you just need to run the migrations.

Run the migrations:

.. code-block:: bash

    piccolo migrations forwards user

Create a new user.

.. code-block:: bash

    piccolo user create

You will be prompted to enter username, email address and password 
(you will be asked to enter your password twice and second time is password confirmation). 
The last step is to confirm that you want to be an administrator. 

.. warning:: 
    You must answer affirmatively because otherwise you will not be able to access the admin interface.

You can also change a user's password with same steps like in user creation.

.. code-block:: bash

    piccolo user change_password
