Multi-factor Authentication
===========================

Piccolo Admin supports Multi-factor Authentication (MFA). See the
``mfa_providers`` argument in :func:`create_admin <piccolo_admin.endpoints.create_admin>`.

We currently recommend using the ``AuthenticatorProvider`` with
``XChaCha20Provider`` for encryption.
