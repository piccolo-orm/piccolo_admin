import uvicorn
from movies.endpoints import HomeEndpoint
from movies.tables import Director, Movie
from starlette.routing import Mount, Route, Router

from piccolo_admin.endpoints import create_admin

# The `allowed_hosts` argument is required when running under HTTPS. It's
# used for additional CSRF defence.
admin = create_admin([Director, Movie], allowed_hosts=["my_site.com"])


router = Router(
    [
        Route(path="/", endpoint=HomeEndpoint),
        Mount(path="/admin/", app=admin),
    ]
)


if __name__ == "__main__":
    uvicorn.run(router)
