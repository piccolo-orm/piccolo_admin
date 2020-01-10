"""
Runs the admin in read only mode - useful for letting people evaluate the admin
online without risk of abuse.
"""
import uvicorn
from piccolo_admin.example import Director, Movie, Sessions, User, create_admin


APP = create_admin(
    [Director, Movie], auth_table=User, session_table=Sessions, read_only=True
)


def main():
    uvicorn.run(APP)


if __name__ == "__main__":
    main()
