Changes
=======

0.19.4
------
Fixed a bug with the z-index of the sidebar on mobile. Thanks to @sinisaos for
discovering this issue.

0.19.3
------
Improved the UI when the network is slow (courtesy @sinisaos).

With ``FormConfig``, if the Pydantic model has a default value provided, this
is rendered in the form UI (thanks to @simplynail for this idea).


0.19.2
------
The ``textarea`` and ``button`` elements were using the browser's default font,
instead of our custom font.

Improved the docstring for ``create_admin``.

0.19.1
------
Fixed a bug where a filter for a column with choices defined would default to
``Null`` instead of ``All``.

0.19.0
------
Added new UI for the foreign key selector.

0.18.2
------
Fixed a bug where resetting the filters in the sidebar would set them to
``less than``. Now they reset to ``equals``. Courtesy @sinisaos.

0.18.1
------
Fixed a bug where a filter for a column with choices would default to
``'Null'`` instead of ``'All'``.

0.18.0
------
Added a ``visible_filters`` option to ``TableConfig``, allowing the user to
specify which filters are shown in the filter sidebar. This is useful if you
have a lot of columns. Courtesy @sinisaos.

Improved the navigation sidebar UI - each section can now be hidden, and the
appearance has been improved when table names are very long. Courtesy
@sinisaos.

Added docs for Javascript formatting to help new contributors.

0.17.0
------
Added ``TableConfig``, which allows more fine grained control over how the
UI behaves for a given ``Table``. Currently it allows you to specify which
columns are visible on the list page, but more options will be added in the
future. Courtesy @sinisaos.

0.16.1
------
Fixed bugs with nullable ``ForeignKey`` and ``Timestamp`` columns - the UI
would try sending back an empty string, instead of a ``null`` value. Courtesy
@sinisaos.

0.16.0
------
JSON values are now displayed in a nicer format in the UI (courtesy @sinisaos).

The popup banner displayed at the bottom of the page will now turn red when
showing an error (it was already green in the past). Courtesy @sinisaos.

0.15.2
------
``FormConfig.endpoint`` now works with async functions.

0.15.1
------
Fixing a bug where setting ``FormConfig.description`` to ``None`` caused a
serialisation error.

0.15.0
------
Added custom forms (courtesy @sinisaos).

It's very easy to use - just provide a Pydantic model, and a function for
handling posted data. Piccolo Admin will then auto generate all of the UI
necessary.

0.14.0
------
Using the ``swagger_ui`` endpoint from Piccolo API for the Swagger docs, so
it works with the CSRF middleware.

0.13.2
------
Rewrote `admin_demo` command to expose configuration options on the command
line.

0.13.1
------
 * Bumped Node dependencies with security warnings.
 * Slightly changed light mode styles (blue-grey sidebar instead of grey).
 * Fixed the `admin_demo` command which is installed by setup.py - the path was
   wrong.

0.13.0
------
Modified the UI to support columns with a ``choices`` attribute set. A select
input element is shown.

0.12.1
------
Fixed issue with ``BigInt`` values being displayed incorrectly.

0.12.0
------
Added support for ``Array`` column type.

0.11.13
-------
Exposing the site name on the login page, courtesy of sinisaos.

0.11.12
-------
Added tooltips using the ``help_text`` attribute on ``Table``.

0.11.11
-------
Added tooltips using the ``help_text`` attribute on ``Column``.

0.11.10
-------
 * The foreign key selector in the add and edit row forms now use the search
   based UI, courtesy of sinisaos.
 * Fixing a Vue JS warning about a route parameter being undefined.

0.11.9
------
 * Exposed the ``host`` and ``port`` options directly in the sandbox CLI.
 * Fixing a bug with read only mode. Was raising a 500 with disallowed HTTPS
   methods

0.11.8
------
 * The foreign key selector in the sidebar is now search based, rather than a
   select element, courtesy of sinisaos. This makes the admin work better with
   very large data sets.
 * Fixed a bug with nullable foreign keys. The value can now be set to null
   without a validation error.

0.11.7
------
Added an ``--inflate`` option to the CLI in example.py. This allows lots of
dummy data to be added during development.

0.11.6
------
Fixing a bug with the date time picker on mobile devices - thanks sinisaos!

0.11.5
------
Fixing a bug where clearing the filters wasn't clearing the duration widget's
value, as it uses a hidden input - thanks sinisaos!

0.11.4
------
Added missing trailing slash to table detail endpoints.

0.11.3
------
Fixing auth API URL - thanks sinisaos!

0.11.2
------
requirements.txt fixes

0.11.1
------
Updated Node dependencies, and fixed requirements clash with FastAPI and
Starlette.

0.11.0
------
 * Refactored ``AdminRouter`` to use ``FastAPI``. This means the API is fully
   documented - courtesy of sinisaos.
 * Moved auth endpoints from ``/api/`` to ``/auth/``, to separate
   auth from the main API.

0.10.9
------
Fixing a bug with fetching meta information from the API (Piccolo version,
site name etc). When a user isn't logged in, it would fail. It now calls the
API again after a successful login - courtesy of sinisaos.

0.10.8
------
 * Can override the nav bar title (defaults to `Piccolo Admin`) - courtesy of
   sinisaos.
 * Other nav bar improvements, such as truncating long usernames.

0.10.7
------
 * Added page size selector - courtesy of sinisaos.
 * Minor fixes

0.10.6
------
Added bulk deletion, and a custom widget for `timedelta` - courtesy of
sinisaos.

0.10.5
------
Added a CSV export button to the row listing - courtesy of sinisaos.

0.10.4
------
 * Removed dependency number for ``uvicorn`` and ``Hypercorn`` - only the very
   high level API is being used, which is unlikely to change, and was causing
   issues for some users when installing via Poetry.
 * Bumped node dependencies.

0.10.3
------
Fixing packaging issues - add Python 3.8 classifier, and missing index.html
file.

0.10.2
------
Subtle UI fixes - page selector, and ``setTimeout`` typo.

0.10.1
------
Added ``allowed_hosts`` argument to ``create_admin`` - otherwise CSRF
middleware will block requests when running under HTTPS.

0.10.0
------
Using latest piccolo, and piccolo_api.

0.9.2
-----
 * Improved pagination when there's lots of data.
 * Bumped node dependencies.

0.9.1
-----
Bumped node requirements because of security warning.

0.9.0
-----
Bumped node and pip requirements.

0.8.1
-----
Bumped node and pip requirements.

0.8.0
-----
Added support for Numeric and Real column types in Piccolo.

0.7.0
-----
Exposing more configuration options for session auth.

0.6.6
-----
Disabling redirect on session auth.

0.6.5
-----
Loosening requirements for Piccolo projects.

0.6.4
-----
Bumped requirements.

0.6.3
-----
Bumped requirements and added apps to piccolo_app migration dependencies.

0.6.2
-----
Converted into a Piccolo app.

0.6.1
-----
Bumped requirements.

0.6.0
-----
Supporting piccolo 0.10.0.

0.5.1
-----
Updated requirements.

0.5.0
-----
Updated dependencies, and vendored remaining Javascript.

0.4.1
-----
Using rate limit middleware on login endpoint. Auto including related tables.
Using PATCH instead of PUT when editing a row. UI improvements.

0.4.0
-----
Using textarea for Text database fields, using new API schema format, and
various UI improvements.

0.3.8
-----
Updated piccolo_api requirements.

0.3.7
-----
UI improvements, and catching 404 errors.

0.3.6
-----
Added 'about' modal to UI.

0.3.5
-----
Updated sandbox - populates data.

0.3.4
-----
Added sandbox, for deploying demo version online.

0.3.3
-----
UI improvements, including light mode. Support for pagination, and operators
in filters.

0.3.2
-----
Fixed typo - missing trailing slash.

0.3.1
-----
Improved auth error handling, and adding defaults automatically when adding
a new row.

0.3.0
-----
Login is working, and various UI improvements.

0.2.0
-----
Updated to work with Piccolo API code layout changes.

0.1.4
-----
Making edit row work.

0.1.3
-----
Added missing assets.

0.1.2
-----
Added missing assets.

0.1.1
-----
Fixing filters.

0.1.0
-----
Initial release.
