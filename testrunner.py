# -*- coding: utf-8 -*-

import sys
import optparse
import logging
import unittest2


USAGE = """%prog SDK_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation"""

SOURCECODE_PATH = 'source'
TESTSCRIPT_PATH = 'testcase'


class LoggerStream(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def flush(self):
        for handler in self.logger.handlers:
            handler.flush()

    def write(self, buf):
        sepos = buf.rfind('\n')

        if sepos != -1:
            content = self.linebuf + buf[:sepos]
            self.linebuf = buf[sepos:].lstrip()

            for line in content.splitlines():
                self.logger.log(self.log_level, line)
        else:
            self.linebuf += buf


def main(sdk_path, test_path):
    #Fix sys path for App Engine SDK
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()

    #Fix sys path for Flask application
    sys.path.insert(0, SOURCECODE_PATH)

    import appengine_config     # Import 3rd party libraries
    logger = logging.getLogger('utlogger')
    logger.info("Start Running TestCases")
    logger.info("")

    stream = LoggerStream(logger, logging.INFO)

    suite = unittest2.loader.TestLoader().discover(test_path)
    unittest2.TextTestRunner(stream, verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) != 1:
        print 'Error: Exactly 1 argument required.'
        parser.print_help()
        sys.exit(1)

    SDK_PATH = args[0]

    main(SDK_PATH, TESTSCRIPT_PATH)
