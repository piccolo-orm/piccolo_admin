# extra

## piccolo_admin

This is an Nginx virtualhost file. It's useful during the development of this
library, as the Vue front end can be run, along with a dummy backend. Since
they will both share the same hostname, session auth works as expected.

Add the piccolo_admin file to the sites-enabled folder on your machine, and
reload Nginx.

Make sure `piccolo_admin` is in your hosts file (/etc/hosts), and maps to
localhost.

Then run the example backend - `python -m piccolo_admin.example`. Also run
Vue CLI - `npm run serve`.

You can then access the app at `piccolo_admin` in your browser.
