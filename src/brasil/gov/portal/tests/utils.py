# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD

import transaction


def login_browser(browser, portal):
    """Autentica usuário de teste no browser"""
    setRoles(portal, TEST_USER_ID, ['Site Administrator'])
    browser.handleErrors = False
    basic_auth = 'Basic {0}'.format(
        '{0}:{1}'.format(TEST_USER_NAME, TEST_USER_PASSWORD),
    )
    browser.addHeader('Authorization', basic_auth)
    transaction.commit()
