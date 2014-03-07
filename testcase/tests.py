# -*- coding: utf-8 -*-

"""
tests.py

"""

import os
import unittest

from google.appengine.ext import testbed

import runner


class DemoTestCase(unittest.TestCase):
    def setUp(self):
        # Flask apps testing. See: http://flask.pocoo.org/docs/testing/
        runner.app.config['TESTING'] = True
        runner.app.config['CSRF_ENABLED'] = False
        self.app = runner.app.test_client()
        # Setups app engine test bed.
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_user_stub()
        self.testbed.init_memcache_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def setCurrentUser(self, email, user_id, is_admin=False):
        os.environ['USER_EMAIL'] = email or ''
        os.environ['USER_ID'] = user_id or ''
        os.environ['USER_IS_ADMIN'] = '1' if is_admin else '0'

    def logoutCurrentUser(self):
        self.setCurrentUser(None, None)

    def test_home(self):
        rv = self.app.get('/')
        assert rv.status == '200 OK'

    def test_says_hello(self):
        rv = self.app.get('/_ex/hello/world')
        assert 'Hello world' in rv.data

    def test_url_redirect(self):
        rv = self.app.get('/_ex')
        assert rv.status == '301 MOVED PERMANENTLY'
        assert 'http://localhost/_ex/' in rv.data

    def test_inserts_data(self):
        self.setCurrentUser(u'john@example.com', u'123')
        rv = self.app.post('/_ex/', data=dict(
            example_name='An example',
            example_description='Description of an example'
        ), follow_redirects=True)
        assert 'Example 1 successfully saved' in rv.data

        rv = self.app.get('/_ex/')
        assert 'No examples yet' not in rv.data
        assert 'An example' in rv.data

    def test_admin_login(self):
        #Anonymous
        rv = self.app.get('/_ex/admin_only')
        assert rv.status == '302 FOUND'
        #Normal user
        self.setCurrentUser(u'john@example.com', u'123')
        rv = self.app.get('/_ex/admin_only')
        assert rv.status == '401 UNAUTHORIZED'
        #Admin
        self.setCurrentUser(u'john@example.com', u'123', True)
        rv = self.app.get('/_ex/admin_only')
        assert rv.status == '200 OK'

    def test_404(self):
        rv = self.app.get('/nonexisturl')
        assert rv.status == '404 NOT FOUND'


if __name__ == '__main__':
    unittest.main()
