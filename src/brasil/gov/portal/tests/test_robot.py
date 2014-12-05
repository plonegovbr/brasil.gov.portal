# -*- coding: utf-8 -*-
from brasil.gov.portal.testing import ACCEPTANCE_TESTING
from plone.testing import layered

import os
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    robot_dir = os.path.join(current_dir, 'robot')
    # Anonymous tests
    tests = [
        os.path.join('robot', doc) for doc in os.listdir(robot_dir)
        if doc.endswith('.robot') and doc.startswith('test_') and 'acessibilidade' not in doc
    ]
    for test in tests:
        suite.addTests([
            layered(
                robotsuite.RobotTestSuite(test),
                layer=ACCEPTANCE_TESTING
            ),
        ])
    return suite
