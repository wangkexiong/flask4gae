# -*- coding: utf-8 -*-

"""
Primary App Engine app handler
"""

import sys
import os
import yaml
import logging.config

package_dir = "packages"
package_dir_path = os.path.join(os.path.dirname(__file__), package_dir)

# Allow unzipped packages to be imported
# from packages folder
sys.path.insert(0, package_dir_path)

# Append zip archives to path for zipimport
for filename in os.listdir(package_dir_path):
    if filename.endswith((".zip", ".egg")):
        sys.path.insert(0, "%s/%s" % (package_dir_path, filename))

# Logging settings
logging.config.dictConfig(yaml.load(open('logging.yaml', 'r')))

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
