Changes
=======

1.9.1
-----

Fixed some bugs with optional fields in custom forms (thanks to @Skelmis for
reporting this).

Improved the contribution docs (thanks to @Skelmis for this).

Improved the MFA docs (thanks to @sinisaos for this).

-------------------------------------------------------------------------------

1.9.0
-----

Forms can now be grouped in the sidebar. This is useful when you have lots of
forms and want to keep things organised. Thanks to @sinisaos for this.

-------------------------------------------------------------------------------

1.8.2
-----

Added a missing JPEG file for an example form.

-------------------------------------------------------------------------------

1.8.1
-----

Added more example forms.

-------------------------------------------------------------------------------

1.8.0
-----

Piccolo Admin forms can now be used to download files, e.g. CSV and PDF files,
which are really useful for reporting purposes. Many thanks to @sinisaos for
the help on this.

-------------------------------------------------------------------------------

1.7.1
-----

Make the `MFA Setup` URL relative, so it works when Piccolo Admin isn't mounted
at the root.

-------------------------------------------------------------------------------

1.7.0
-----

Initial release for Multi-factor Authentication support.

Many thanks to @sinisaos and @Skelmis for their help with this.

-------------------------------------------------------------------------------

1.6.0
-----

When downloading a CSV file from the row listing page, you can now specify
which columns you want to download.

-------------------------------------------------------------------------------

1.5.0
-----

On the add row and edit row forms, the save button is now temporarily disabled
after being pressed (until the API call finishes). This is to prevent a user
from accidentally clicking the button multiple times. Thanks to @sinisaos for
helping with this.

-------------------------------------------------------------------------------

1.4.0
-----

Improved the array widget for arrays of ``Time`` / ``Date`` / ``Timestamp`` /
``Timestamptz``.

-------------------------------------------------------------------------------

1.3.3
-----

Fixed a bug with array inputs in custom forms (thanks to @sinisaos for this).

-------------------------------------------------------------------------------

1.3.2
-----

Added CSP (Content Security Policy) middleware to stop malicious SVG files from
executing JavaScript. This was possible if:

* Local media storage was enabled
* SVG uploads were allowed from untrusted sources
* When viewing an uploaded SVG in Piccolo Admin, if you open the SVG in a new
  tab then it's possible for JavaScript embedded in the SVG file to run.

It's recommended that you upgrade to this version. Thanks to @Skelmis for this.

-------------------------------------------------------------------------------

1.3.1
-----

Fixed a bug with the bulk update button not being translated.

Thanks to @jrycw for reporting the issue, and @sinisaos for the fix.

-------------------------------------------------------------------------------

1.3.0
-----

Added translations for Traditional Chinese (thanks to @jrycw for this).

-------------------------------------------------------------------------------

1.2.2
-----

Fixed a bug with filtering ``Array`` columns when choices are defined. Thanks
to @sinisaos for discovering the solution.

-------------------------------------------------------------------------------

1.2.1
-----

Fixed a bug with ``Array`` columns which have choices defined. Both a
``select`` and ``input`` widget were being shown.

-------------------------------------------------------------------------------

1.2.0
-----

Added Python 3.12 support.

When filtering ``Varchar`` and ``Text`` columns, you can now specify the
``match``. Previously, it always defaulted to ``contains``, but now you can
specify ``starts``, ``ends`` and ``exact``. For example, you can now filter for
a movie with a name starting with ``Star Wars``.

When filtering numeric / date / time columns, you can now specify the
``not equals`` operator. For example, give me all the movie tickets which
aren't on a certain day.

Fixed some minor bugs, and added additional Playwright tests.

-------------------------------------------------------------------------------

1.1.3
-----

Improved CSV downloads - the user now has the option of using commas or
semicolons as delimiters. In Piccolo Admin v1 we had changed to using
semicolons by default, which was causing confusion.

-------------------------------------------------------------------------------

1.1.2
-----

The sidebar styles were improved (see
`this issue <https://github.com/piccolo-orm/piccolo_admin/issues/342>`_ for more
info).

-------------------------------------------------------------------------------

1.1.1
-----

Fixed a regression in Piccolo Admin v1, where nullable boolean fields defaulted
to ``null`` instead of ``all`` in the filter sidebar. This was caused by
changes in Pydantic v2, where the JSON schema changed.

-------------------------------------------------------------------------------

1.1.0
-----

Big improvements to ``Timestamptz`` columns:

* Piccolo Admin now displays the timezone in the UI.
* The resolution of the widget can be specified using ``TableConfig.time_resolution``,
  so you can decide if the user can pick seconds / milliseconds.

-------------------------------------------------------------------------------

1.0.0
-----

Updated to work with Piccolo v1 (which uses Pydantic v2).

The front end code has also been substantially upgraded to Vue v3.

-------------------------------------------------------------------------------

0.58.0
------

The default rate limiting is now more aggressive. This can be overridden using
the ``rate_limit_provider`` argument of ``create_admin``.

-------------------------------------------------------------------------------

0.57.0
------

Improved the handling of nullable ``Varchar`` / ``Text`` columns in the UI.

-------------------------------------------------------------------------------

0.56.0
------

Improved the handling of nullable ``JSON`` / ``JSONB`` columns in the UI.

-------------------------------------------------------------------------------

0.55.0
------

When deleting a row, if a problem is encountered then an error message is now
shown in the UI.

This is useful if we have constraints on the table (for example
``ON DELETE RESTRICT``).

Support for Python 3.7 was dropped as it's now end of life.

-------------------------------------------------------------------------------

0.54.0
------

Improved the behaviour of the `referencing tables` links on the detail page.

-------------------------------------------------------------------------------

0.53.0
------

Improved the UI for JSON fields (the cursor would sometimes jump to the
bottom).

-------------------------------------------------------------------------------

0.52.0
------

Version pinning Pydantic to v1, as v2 has breaking changes.

We will add support for Pydantic v2 in a future release.

Thanks to @sinisaos for helping with this.

-------------------------------------------------------------------------------

0.51.0
------

Improved the UI for password inputs (e.g. on the change password page). Thanks
to @sinisaos for this.

Fixed a bug with nullable date fields.

-------------------------------------------------------------------------------

0.50.0
------

Improved handling of nullable email fields.

Thanks to @sinisaos for adding this.

-------------------------------------------------------------------------------

0.49.0
------

Custom links can now be added to the sidebar. This allows quick navigation to
specific pages in the admin, or to external websites. For example:

.. code-block:: python

  create_admin(
      sidebar_links={
          "Top Movies": "/admin/#/movies/?__order=-popularity",
      }
      ...
  )

Thanks to @sinisaos for adding this.

-------------------------------------------------------------------------------

0.48.0
------

* Improved the type annotations for ``FormConfig``.
* Fixed a bug with array fields in custom forms (thanks to @sinisaos for
  fixing this).

-------------------------------------------------------------------------------

0.47.0
------

Multiple columns can now be used for sorting the rows in the UI.

Setting the default order for a table is now possible. For example, if we want
to order movies by rating:

.. code-block:: python

  create_admin(
      tables=[
          TableConfig(
              Movie,
              order_by=[
                  OrderBy(Movie.rating, ascending=False)
              ]
          )
      )
  )

Thanks to @sinisaos and @sumitsharansatsangi for their help with this.

-------------------------------------------------------------------------------

0.46.0
------

Added Turkish translations (thanks to @omerucel for this).

-------------------------------------------------------------------------------

0.45.2
------

Nullable UUID fields now work correctly.

-------------------------------------------------------------------------------

0.45.1
------

Add back JSON formatting in list view which was removed by accident.

-------------------------------------------------------------------------------

0.45.0
------

Nullable number fields now work correctly.

-------------------------------------------------------------------------------

0.44.0
------

Fixed a bug with nullable ``Boolean`` columns - filtering wasn't working in the
sidebar.

-------------------------------------------------------------------------------

0.43.0
------

Added the ``link_column`` option to ``TableConfig``. By default, the primary key
is used in the list view of Piccolo Admin to link to the edit page. Using
``link_column`` you can specify a different column (for example, if you hid
the primary key using ``visible_columns``). Thanks to @sinisaos for helping
with this.

-------------------------------------------------------------------------------

0.42.0
------

Tables can now be grouped in the sidebar - this is helpful if you have lots of
tables. To do this, use the ``menu_group`` argument of ``TableConfig``.

Thanks to @sinisaos and @sumitsharansatsangi for their help with this.

-------------------------------------------------------------------------------

0.41.0
------

A fix to make Piccolo Admin work with ``fastapi>=0.89.0``.

-------------------------------------------------------------------------------

0.40.0
------

* Improved German translations (thanks to @hblunck for this).
* When submitting a form, scroll to the top of the page if an error occurs so
  the error box is visible (thanks to @sinisaos for this).
* If a custom ``BaseUser`` table is used for authentication, which uses a
  ``UUID`` as the primary key, it now works.

-------------------------------------------------------------------------------

0.39.0
------

If an ``Array`` column has ``choices`` specified, then Piccolo Admin will
show dropdowns, so the user can pick one of the choices.

-------------------------------------------------------------------------------

0.38.0
------

Fixed a bug with ``TableConfig`` and ``exclude_visible_columns``. Thanks to
@web-maker for this fix.

-------------------------------------------------------------------------------

0.37.0
------

* Python 3.11 is now officially supported.
* Added debug mode: ``create_admin(tables=[MyTable], debug=True)``.
* Logging exceptions for 500 errors.
* Fixed a typo in the docs about how to use validators (thanks to @sinisaos for
  reporting this).
* Updated the tests for Starlette / FastAPI's new test client. This means that
  ``fastapi==0.87.0`` / ``starlette==0.21.0`` are now the minimum versions
  supported. Thanks to @sinisaos for this.

-------------------------------------------------------------------------------

0.36.0
------

Lots of small enhancements.

* Fixed bugs with the foreign key selector. Sometimes the edit button didn't
  work. Also, sometimes the value shown in the input box wasn't refreshing when
  navigating to a new page.
* The HTML title now matches the ``site_name`` parameter in ``create_admin``
  (thanks to @sinisaos for this).
* Updated Vue to the latest version.
* Internal code refactoring.

-------------------------------------------------------------------------------

0.35.0
------

``Validators`` can now be specified in ``TableConfig``.

This allows fine grained access control - for example, only allowing some users
to send ``POST`` requests to certain API endpoints:

.. code-block:: python

  from piccolo_api.crud.endpoints import PiccoloCRUD
  from starlette.exceptions import HTTPException
  from starlette.requests import Request


  async def manager_only(
      piccolo_crud: PiccoloCRUD,
      request: Request
  ):
      # The Piccolo `BaseUser` can be accessed from the request.
      user = request.user.user

      # Assuming we have another database table where we record
      # users with certain permissions.
      manager = await Manager.exists().where(manager.user == user)

      if not manager:
          # Raise a Starlette exception if we want to reject the
          # request.
          raise HTTPException(
              status_code=403,
              detail="Only managers are allowed to do this"
          )


  admin = create_admin(
      tables=TableConfig(
          Movie,
          validators=Validators(post_single=[manager_only])
      )
  )

-------------------------------------------------------------------------------

0.34.0
------

Updated the date / datetime / time picker.

-------------------------------------------------------------------------------

0.33.1
------

Fixed an issue with installing ``piccolo_admin`` in editable mode with ``pip``.

Thanks to @peterschutt for reporting this issue.

-------------------------------------------------------------------------------

0.33.0
------

Improved the UI for error messages. Thanks to @sinisaos for adding this.

-------------------------------------------------------------------------------

0.32.0
------

Camelcase column names could break parts of Piccolo Admin. It now works as
expected:

.. code-block:: python

  class Person(Table):
      # This now works:
      firstName = Varchar()

Even though camelcase is unusual in Python, a user may be using an existing
database, so it makes sense to support it. Thanks to @sumitsharansatsangi for
reporting this issue.

-------------------------------------------------------------------------------

0.31.2
------

When ``piccolo_admin`` is installed, an ``admin_demo`` script is made available
on the command line, which launches a Piccolo Admin demo.

It wasn't working due to a missing folder, which has now been fixed.

-------------------------------------------------------------------------------

0.31.1
------

Fixed a bug with custom forms - under some situations they would fail to
render. Thanks to @sinisaos for discovering this issue. See
`PR 208 <https://github.com/piccolo-orm/piccolo_admin/pull/208>`_ for more
info.

-------------------------------------------------------------------------------

0.31.0
------

Improved the French translations (courtesy @LeMeteore).

-------------------------------------------------------------------------------

0.30.0
------

Added translations for simplified Chinese characters (courtesy @mnixry).

-------------------------------------------------------------------------------

0.29.1
------

The media endpoints now obey the ``read_only`` option of ``create_admin``.
Read only mode is used for online demos.

Thanks to @sinisaos for adding this.

-------------------------------------------------------------------------------

0.29.0
------

Added media upload support - to both a local folder, and S3.

Images, videos, PDFs, and audio files can be viewed within the UI.

This is the one of the biggest updates we've ever made!

Thanks to @sinisaos for all of the help.

-------------------------------------------------------------------------------

0.28.0
------

Added Ukrainian translations (courtesy @ruslan-rv-ua).

-------------------------------------------------------------------------------

0.27.0
------

Added Russian translations (courtesy @northpowered).

-------------------------------------------------------------------------------

0.26.1
------

Modified the release process, so it works on GitHub (courtesy @olliglorioso).

-------------------------------------------------------------------------------

0.26.0
------

Added Finnish translations (courtesy @olliglorioso).

-------------------------------------------------------------------------------

0.25.0
------

Added translations, to make the UI more accessible in a variety of languages
(thanks to @sinisaos for helping with this).

-------------------------------------------------------------------------------

0.24.0
------

``TableConfig`` now has a ``hooks`` argument - so custom logic can be run when
a row is added / deleted / modified. Thanks to @Anton-Karpenko for suggesting
this feature.

-------------------------------------------------------------------------------

0.23.0
------

The WYSIWYG editor we use for ``rich_text_columns`` has been modified, so the
user can now create HTML headings. Thanks to @tigerline86 for suggesting this
feature and @sinisaos for implementing it.

Rows can now be bulk modified - for example, if you have 100 blog posts which
need converting to ``draft=False``, it can now be easily done using the
Piccolo Admin GUI in a single operation (courtesy @sinisaos).

-------------------------------------------------------------------------------

0.22.2
------

More sandbox fixes.

-------------------------------------------------------------------------------

0.22.1
------

Fixed a bug with the sandbox.

-------------------------------------------------------------------------------

0.22.0
------

The user can now change their password in the Piccolo Admin UI (courtesy
@sinisaos).

After submitting a custom form with Piccolo Admin, the UI used to show the
response message in a popup at the bottom of the screen. It now shows a success
page instead, which is better if the response message is long, as it's easier
for the user to read. Thanks to @ethagnawl for reporting this issue.

-------------------------------------------------------------------------------

0.21.0
------

Added a warning if a Piccolo ``Table`` column is both ``secret=True`` and
``required=True``, as it's unsupported by Piccolo admin (courtesy @ethagnawl).

-------------------------------------------------------------------------------

0.20.0
------

You can now use a rich text editor for ``Text`` columns (courtesy @sinisaos).

.. code-block:: python

    from piccolo_admin.endpoints import TableConfig

    from movies.tables import Movie

    movie_config = TableConfig(
        Movie,
        rich_text_columns=[
            Movie.description
        ]
    )

    create_admin(movie_config)

This is useful when using Piccolo Admin for authoring content in blogs etc.

-------------------------------------------------------------------------------

0.19.6
------
Fixes for ``Table`` classes which have custom primary key columns.

-------------------------------------------------------------------------------

0.19.5
------
More z-index refinements (thanks @sinisaos).

-------------------------------------------------------------------------------

0.19.4
------
Fixed a bug with the z-index of the sidebar on mobile. Thanks to @sinisaos for
discovering this issue.

-------------------------------------------------------------------------------

0.19.3
------
Improved the UI when the network is slow (courtesy @sinisaos).

With ``FormConfig``, if the Pydantic model has a default value provided, this
is rendered in the form UI (thanks to @simplynail for this idea).

-------------------------------------------------------------------------------

0.19.2
------
The ``textarea`` and ``button`` elements were using the browser's default font,
instead of our custom font.

Improved the docstring for ``create_admin``.

-------------------------------------------------------------------------------

0.19.1
------
Fixed a bug where a filter for a column with choices defined would default to
``Null`` instead of ``All``.

-------------------------------------------------------------------------------

0.19.0
------
Added new UI for the foreign key selector.

-------------------------------------------------------------------------------

0.18.2
------
Fixed a bug where resetting the filters in the sidebar would set them to
``less than``. Now they reset to ``equals``. Courtesy @sinisaos.

-------------------------------------------------------------------------------

0.18.1
------
Fixed a bug where a filter for a column with choices would default to
``'Null'`` instead of ``'All'``.

-------------------------------------------------------------------------------

0.18.0
------
Added a ``visible_filters`` option to ``TableConfig``, allowing the user to
specify which filters are shown in the filter sidebar. This is useful if you
have a lot of columns. Courtesy @sinisaos.

Improved the navigation sidebar UI - each section can now be hidden, and the
appearance has been improved when table names are very long. Courtesy
@sinisaos.

Added docs for Javascript formatting to help new contributors.

-------------------------------------------------------------------------------

0.17.0
------
Added ``TableConfig``, which allows more fine grained control over how the
UI behaves for a given ``Table``. Currently it allows you to specify which
columns are visible on the list page, but more options will be added in the
future. Courtesy @sinisaos.

-------------------------------------------------------------------------------

0.16.1
------
Fixed bugs with nullable ``ForeignKey`` and ``Timestamp`` columns - the UI
would try sending back an empty string, instead of a ``null`` value. Courtesy
@sinisaos.

-------------------------------------------------------------------------------

0.16.0
------
JSON values are now displayed in a nicer format in the UI (courtesy @sinisaos).

The popup banner displayed at the bottom of the page will now turn red when
showing an error (it was already green in the past). Courtesy @sinisaos.

-------------------------------------------------------------------------------

0.15.2
------
``FormConfig.endpoint`` now works with async functions.

-------------------------------------------------------------------------------

0.15.1
------
Fixing a bug where setting ``FormConfig.description`` to ``None`` caused a
serialisation error.

-------------------------------------------------------------------------------

0.15.0
------
Added custom forms (courtesy @sinisaos).

It's very easy to use - just provide a Pydantic model, and a function for
handling posted data. Piccolo Admin will then auto generate all of the UI
necessary.

-------------------------------------------------------------------------------

0.14.0
------
Using the ``swagger_ui`` endpoint from Piccolo API for the Swagger docs, so
it works with the CSRF middleware.

-------------------------------------------------------------------------------

0.13.2
------
Rewrote `admin_demo` command to expose configuration options on the command
line.

-------------------------------------------------------------------------------

0.13.1
------
* Bumped Node dependencies with security warnings.
* Slightly changed light mode styles (blue-grey sidebar instead of grey).
* Fixed the `admin_demo` command which is installed by setup.py - the path was
  wrong.

-------------------------------------------------------------------------------

0.13.0
------
Modified the UI to support columns with a ``choices`` attribute set. A select
input element is shown.

-------------------------------------------------------------------------------

0.12.1
------
Fixed issue with ``BigInt`` values being displayed incorrectly.

-------------------------------------------------------------------------------

0.12.0
------
Added support for ``Array`` column type.

-------------------------------------------------------------------------------

0.11.13
-------
Exposing the site name on the login page, courtesy of sinisaos.

-------------------------------------------------------------------------------

0.11.12
-------
Added tooltips using the ``help_text`` attribute on ``Table``.

-------------------------------------------------------------------------------

0.11.11
-------
Added tooltips using the ``help_text`` attribute on ``Column``.

-------------------------------------------------------------------------------

0.11.10
-------
* The foreign key selector in the add and edit row forms now use the search
  based UI, courtesy of sinisaos.
* Fixing a Vue JS warning about a route parameter being undefined.

-------------------------------------------------------------------------------

0.11.9
------
* Exposed the ``host`` and ``port`` options directly in the sandbox CLI.
* Fixing a bug with read only mode. Was raising a 500 with disallowed HTTPS
  methods

-------------------------------------------------------------------------------

0.11.8
------
* The foreign key selector in the sidebar is now search based, rather than a
  select element, courtesy of sinisaos. This makes the admin work better with
  very large data sets.
* Fixed a bug with nullable foreign keys. The value can now be set to null
  without a validation error.

-------------------------------------------------------------------------------

0.11.7
------
Added an ``--inflate`` option to the CLI in example.py. This allows lots of
dummy data to be added during development.

-------------------------------------------------------------------------------

0.11.6
------
Fixing a bug with the date time picker on mobile devices - thanks sinisaos!

-------------------------------------------------------------------------------

0.11.5
------
Fixing a bug where clearing the filters wasn't clearing the duration widget's
value, as it uses a hidden input - thanks sinisaos!

-------------------------------------------------------------------------------

0.11.4
------
Added missing trailing slash to table detail endpoints.

-------------------------------------------------------------------------------

0.11.3
------
Fixing auth API URL - thanks sinisaos!

-------------------------------------------------------------------------------

0.11.2
------
requirements.txt fixes

-------------------------------------------------------------------------------

0.11.1
------
Updated Node dependencies, and fixed requirements clash with FastAPI and
Starlette.

-------------------------------------------------------------------------------

0.11.0
------
* Refactored ``AdminRouter`` to use ``FastAPI``. This means the API is fully
  documented - courtesy of sinisaos.
* Moved auth endpoints from ``/api/`` to ``/auth/``, to separate
  auth from the main API.

-------------------------------------------------------------------------------

0.10.9
------
Fixing a bug with fetching meta information from the API (Piccolo version,
site name etc). When a user isn't logged in, it would fail. It now calls the
API again after a successful login - courtesy of sinisaos.

-------------------------------------------------------------------------------

0.10.8
------
* Can override the nav bar title (defaults to `Piccolo Admin`) - courtesy of
  sinisaos.
* Other nav bar improvements, such as truncating long usernames.

-------------------------------------------------------------------------------

0.10.7
------
* Added page size selector - courtesy of sinisaos.
* Minor fixes

-------------------------------------------------------------------------------

0.10.6
------
Added bulk deletion, and a custom widget for `timedelta` - courtesy of
sinisaos.

-------------------------------------------------------------------------------

0.10.5
------
Added a CSV export button to the row listing - courtesy of sinisaos.

-------------------------------------------------------------------------------

0.10.4
------
* Removed dependency number for ``uvicorn`` and ``Hypercorn`` - only the very
  high level API is being used, which is unlikely to change, and was causing
  issues for some users when installing via Poetry.
* Bumped node dependencies.

-------------------------------------------------------------------------------

0.10.3
------
Fixing packaging issues - add Python 3.8 classifier, and missing index.html
file.

-------------------------------------------------------------------------------

0.10.2
------
Subtle UI fixes - page selector, and ``setTimeout`` typo.

-------------------------------------------------------------------------------

0.10.1
------
Added ``allowed_hosts`` argument to ``create_admin`` - otherwise CSRF
middleware will block requests when running under HTTPS.

-------------------------------------------------------------------------------

0.10.0
------
Using latest piccolo, and piccolo_api.

-------------------------------------------------------------------------------

0.9.2
-----
* Improved pagination when there's lots of data.
* Bumped node dependencies.

-------------------------------------------------------------------------------

0.9.1
-----
Bumped node requirements because of security warning.

-------------------------------------------------------------------------------

0.9.0
-----
Bumped node and pip requirements.

-------------------------------------------------------------------------------

0.8.1
-----
Bumped node and pip requirements.

-------------------------------------------------------------------------------

0.8.0
-----
Added support for Numeric and Real column types in Piccolo.

-------------------------------------------------------------------------------

0.7.0
-----
Exposing more configuration options for session auth.

-------------------------------------------------------------------------------

0.6.6
-----
Disabling redirect on session auth.

-------------------------------------------------------------------------------

0.6.5
-----
Loosening requirements for Piccolo projects.

-------------------------------------------------------------------------------

0.6.4
-----
Bumped requirements.

-------------------------------------------------------------------------------

0.6.3
-----
Bumped requirements and added apps to piccolo_app migration dependencies.

-------------------------------------------------------------------------------

0.6.2
-----
Converted into a Piccolo app.

-------------------------------------------------------------------------------

0.6.1
-----
Bumped requirements.

-------------------------------------------------------------------------------

0.6.0
-----
Supporting piccolo 0.10.0.

-------------------------------------------------------------------------------

0.5.1
-----
Updated requirements.

-------------------------------------------------------------------------------

0.5.0
-----
Updated dependencies, and vendored remaining Javascript.

-------------------------------------------------------------------------------

0.4.1
-----
Using rate limit middleware on login endpoint. Auto including related tables.
Using PATCH instead of PUT when editing a row. UI improvements.

-------------------------------------------------------------------------------

0.4.0
-----
Using textarea for Text database fields, using new API schema format, and
various UI improvements.

-------------------------------------------------------------------------------

0.3.8
-----
Updated piccolo_api requirements.

-------------------------------------------------------------------------------

0.3.7
-----
UI improvements, and catching 404 errors.

-------------------------------------------------------------------------------

0.3.6
-----
Added 'about' modal to UI.

-------------------------------------------------------------------------------

0.3.5
-----
Updated sandbox - populates data.

-------------------------------------------------------------------------------

0.3.4
-----
Added sandbox, for deploying demo version online.

-------------------------------------------------------------------------------

0.3.3
-----
UI improvements, including light mode. Support for pagination, and operators
in filters.

-------------------------------------------------------------------------------

0.3.2
-----
Fixed typo - missing trailing slash.

-------------------------------------------------------------------------------

0.3.1
-----
Improved auth error handling, and adding defaults automatically when adding
a new row.

-------------------------------------------------------------------------------

0.3.0
-----
Login is working, and various UI improvements.

-------------------------------------------------------------------------------

0.2.0
-----
Updated to work with Piccolo API code layout changes.

-------------------------------------------------------------------------------

0.1.4
-----
Making edit row work.

-------------------------------------------------------------------------------

0.1.3
-----
Added missing assets.

-------------------------------------------------------------------------------

0.1.2
-----
Added missing assets.

-------------------------------------------------------------------------------

0.1.1
-----
Fixing filters.

-------------------------------------------------------------------------------

0.1.0
-----
Initial release.
