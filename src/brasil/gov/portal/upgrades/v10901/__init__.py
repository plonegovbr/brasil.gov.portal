# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


def remove_portlet_assignments(obj):
    """Remove portlet assignments on object."""
    from plone.portlets.interfaces import ILocalPortletAssignable
    from plone.portlets.interfaces import IPortletAssignmentMapping
    from plone.portlets.interfaces import IPortletManager
    from zope.component import getMultiAdapter
    from zope.component import getUtility
    if not ILocalPortletAssignable.providedBy(obj):
        return
    for name in ('plone.leftcolumn', 'plone.rightcolumn'):
        manager = getUtility(IPortletManager, name=name)
        mapping = getMultiAdapter((obj, manager), IPortletAssignmentMapping)
        for i in mapping.keys():
            logger.info('Removing portlet assignment in "{0}"'.format(obj))
            del mapping[i]


def remove_root_portlets(setup_tool):
    """Remove portlet assigments at portal root."""
    remove_portlet_assignments(api.portal.get())
