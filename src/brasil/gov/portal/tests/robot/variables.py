# -*- coding: utf-8 -*-
from brasil.gov.portal import tests
from plone.app.testing.interfaces import PLONE_SITE_ID

import os


PORT = os.environ.get('ZSERVER_PORT', 55001)
PORT = os.environ.get('PLONE_TESTING_PORT', PORT)
ZSERVER_PORT = PORT
SELENIUM_IMPLICIT_WAIT = os.environ.get('SELENIUM_IMPLICIT_WAIT', '0.1s')
SELENIUM_TIMEOUT = os.environ.get('SELENIUM_IMPLICIT_WAIT', '20s')

ZOPE_HOST = os.environ.get('ZOPE_HOST', 'localhost')
ZOPE_URL = os.environ.get('ZOPE_URL', 'http://%s:%s' % (ZOPE_HOST, PORT))
ZOPE_LOGGED_URL = os.environ.get('ZOPE_URL', 'http://admin:secret@%s:%s' %
                                 (ZOPE_HOST, PORT))
NOVO_SITE_URL = '%s/@@plone-addsite?site_id=Plone' % ZOPE_LOGGED_URL
PLONE_SITE_ID = os.environ.get('PLONE_SITE_ID', PLONE_SITE_ID)
PLONE_URL = os.environ.get('PLONE_URL', '%s/%s' % (ZOPE_URL, PLONE_SITE_ID))
BROWSER = os.environ.get('BROWSER', 'Firefox')
REMOTE_URL = os.environ.get('REMOTE_URL', '')
DESIRED_CAPABILITIES = os.environ.get('DESIRED_CAPABILITIES', '')

TEST_FOLDER = os.environ.get('TEST_FOLDER', '%s/test-folder' % PLONE_URL)
FF_PROFILE = os.path.join(os.path.dirname(tests.__file__),
                          'robot/ff_profile')
