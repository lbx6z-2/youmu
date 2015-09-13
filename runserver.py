#!/usr/bin/python

from youmu import create_app

app = create_app()
app.run(host = "0.0.0.0", debug = True, threaded = True)
