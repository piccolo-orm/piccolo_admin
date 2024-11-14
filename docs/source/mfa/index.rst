Multi-factor Authentication
===========================

Piccolo Admin supports Multi-factor Authentication (MFA). See the
``mfa_providers`` argument in :func:`create_admin <piccolo_admin.endpoints.create_admin>`.

Most of the underlying functionality comes from ``piccolo_api``.

.. note::

   There is a `video tutorial on YouTube <https://youtu.be/S24JoFdWxwQ>`__.

``MFAProvider``
---------------

We currently recommend using the :class:`AuthenticatorProvider <piccolo_api.mfa.authenticator.provider.AuthenticatorProvider>`
(which uses an authenticator app for generating codes) with
:class:`XChaCha20Provider <piccolo_api.encryption.providers.XChaCha20Provider>`
for encryption.

You can also implement your own subclass of :class:`MFAProvider <piccolo_api.mfa.provider.MFAProvider>`
if you want to do something custom.

Example
-------

.. code-block:: python

    from piccolo_admin.endpoints import create_admin
    from piccolo_api.encryption.providers import XChaCha20Provider
    from piccolo_api.mfa.authenticator.provider import AuthenticatorProvider


    app = create_admin(
        ...,
        mfa_providers=[
            AuthenticatorProvider(
                encryption_provider=XChaCha20Provider(
                    encryption_key=(
                        b"my_encryption_key"
                    )
                ),
            )
        ]
    )

To generate the encryption key in the above example:

.. code-block:: pycon

    >>> from piccolo_api.encryption.providers import XChaCha20Provider
    >>> XChaCha20Provider.get_new_key()
    b'\xcd6\xaf\xef\x83\xbf@\xda\x06q\x8c=p\xe8\xe8Q\xa2\x01\x1bW$\xf6\xa2AC61\x0erN\xa9\x1c'

.. note::
    Piccolo Admin currently allows you to use a single ``MFAProvider``, but
    this might change in the future.

Install dependencies
--------------------

For the above example, you need to install some extra dependencies:

.. code-block:: bash

    pip install piccolo_api[authenticator,pynacl]

Create database table
---------------------

You need to create the database table for storing the MFA secrets, either by:

* Adding ``"piccolo_api.mfa.authenticator.piccolo_app"`` to your ``AppRegistry``
  in ``piccolo_conf.py``, then running the migrations using
  ``piccolo migrations forwards all``.
* Manually creating the table.

  .. code-block:: pycon

    >>> from piccolo_api.mfa.authenticator.tables import AuthenticatorSecret
    >>> AuthenticatorSecret.create_table().run_sync()
