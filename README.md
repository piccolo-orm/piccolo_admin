# Piccolo Admin

piccolo_admin provides a simple yet powerful admin interface on top of Piccolo models - allowing you to easily add / edit / filter your data.

![Screenshot](https://raw.githubusercontent.com/piccolo-orm/piccolo_admin/master/docs/images/screenshot.png "Screenshot")

## Try it

[Try it online](https://demo1.piccolo-orm.com/) (username: piccolo, password: piccolo123).

## Local Demo

To run a demo locally, using Python 3.7 or above:

```bash
pip install piccolo_admin
admin_demo
```

And then just launch `localhost:8000` in your browser.

To see what happens behind the scenes, see `piccolo_admin/example.py`.

In a few lines of code we are able to:

 * Define our models
 * Setup a database
 * Create a REST API
 * Setup a web server and admin interface

## ASGI

Since the admin is an ASGI app, you can either run it standalone like in the demo, or integrate it with a larger ASGI app.

For example, using Starlette routes:

```python
from piccolo_admin.endpoints import create_admin
from starlette.routing import Router, Route
import uvicorn

from my_project.tables import Director, Movie


# The `allowed_hosts` argument is required when running under HTTPS. It's used
# for additional CSRF defence.
admin = create_admin([Director, Movie], allowed_hosts=['my_site.com'])


router = Router([
    Route(path="/", endpoint=Hello),
    Mount(path="/admin/", app=admin),
])


if __name__ == '__main__':
    uvicorn.run(router)

```

## Session table

The admin uses session auth, which requires a database table.

Add `piccolo_admin.piccolo_app` to the APP_REGISTRY in your piccolo_conf.py
project file, then run:

```bash
piccolo migrations forwards session_auth
```

To learn more about the Piccolo project files, check out the [docs](https://piccolo-orm.readthedocs.io/en/latest/piccolo/projects_and_apps/piccolo_apps.html).


## Contributing

The backend is just vanilla Python.

The front end is built using Vue.js. To make modifications, clone the repo, and cd into the `admin_ui` directory.

Install the npm dependencies:

```bash
npm install
```

And then you can launch the admin as follows:

```bash
npm run serve
```

It will auto refresh the UI as you make changes to the source files.

The UI needs an API to interact with - the easiest way to do this is to use the demo app.

```bash
admin_demo

# Or alternatively
python -m piccolo_admin.example
```

You will need to configure a local webserver as a proxy - see extra/piccolo_admin.
