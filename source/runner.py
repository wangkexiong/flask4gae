# -*- coding: utf-8 -*-

"""
Primary App Engine app handler
"""

from wsgiref.handlers import CGIHandler
from application.settings import DEBUG_MODE
from application import create_app

app = create_app()


def main():
    if DEBUG_MODE:
        # Run debugged app
        from werkzeug_debugger_appengine import get_debugged_app
        app.debug = True
        debugged_app = get_debugged_app(app)
        CGIHandler().run(debugged_app)
    else:
        # Run production app
        from google.appengine.ext.webapp.util import run_wsgi_app
        run_wsgi_app(app)


# Use App Engine app caching
if __name__ == "__main__":
    main()
