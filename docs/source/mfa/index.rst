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
