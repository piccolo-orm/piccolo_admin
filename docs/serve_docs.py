#!/usr/bin/env python
from livereload import Server, shell


server = Server()
server.watch("source/", shell("make html"))
server.watch("../piccolo_admin", shell("make html"))
server.serve(root="build/html")
