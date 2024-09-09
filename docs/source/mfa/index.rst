Multi-factor Authentication
===========================

Piccolo Admin supports Multi-factor Authentication (MFA). See the
``mfa_providers`` argument in :func:`create_admin <piccolo_admin.endpoints.create_admin>`.

Most of the underlying functionality comes from ``piccolo_api``.

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
    >>> XChaCha20Provider.generate_key()
    b'\xb7(\xa5\xa6\xa4&\xeb\x8eI\xfe_Y\x16\x12\xf4\xf4\xa8|\xc6#\xd1\x02\xa2s\x03]\xea\x12\xb9\xf1\xa2\xb3'

.. note::
    Piccolo Admin currently allows you to use a single ``MFAProvider``, but
    this might change in the future.
