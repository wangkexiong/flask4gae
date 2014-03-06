# -*- coding: utf-8 -*-

import optparse
import sys
import unittest2


USAGE = """%prog SDK_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation"""

SOURCECODE_PATH = 'source'
TESTSCRIPT_PATH = 'testcase'


def main(sdk_path, test_path):
    #Fix sys path for App Engine SDK
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()

    #Fix sys path for Flask application
    sys.path.insert(0, SOURCECODE_PATH)

    import appengine_config     # Import 3rd party libraries
    import logging
    logger = logging.getLogger('utlogger')
    logger.info("Start Running TestCases")

    suite = unittest2.loader.TestLoader().discover(test_path)
    unittest2.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) != 1:
        print 'Error: Exactly 1 argument required.'
        parser.print_help()
        sys.exit(1)

    SDK_PATH = args[0]

    main(SDK_PATH, TESTSCRIPT_PATH)
