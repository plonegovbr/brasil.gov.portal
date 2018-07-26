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
            logger.info('Removing portlet "{0}" from {1}'.format(i, obj))
            del mapping[i]


def remove_root_portlets(setup_tool):
    """Remove portlet assigments at portal root."""
    remove_portlet_assignments(api.portal.get())
    logger.info('Portlet assignments removed from portal root')


def get_valid_objects(**kw):
    """Generate a list of objects associated with valid brains."""
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog(**kw)
    logger.info('Found {0} objects in the catalog'.format(len(results)))
    for b in results:
        try:
            obj = b.getObject()
        except (AttributeError, KeyError):
            obj = None

        if obj is None:  # warn on broken entries in the catalog
            msg = 'Invalid object reference in the catalog: {0}'
            logger.warn(msg.format(b.getPath()))
            continue

        yield obj


def fix_cover_columns(setup_tool):
    """Fix column widths on cover objects. Resulting width depends on
    the number of columns in a row (width = 12 / columns).
    """

    import json

    def fix_column_width(layout, columns=1):
        """Traverse the layout tree and fix columns width."""
        new_layout = []
        for e in layout:
            if 'column-size' in e:
                e['column-size'] = 12 // columns
            if e['type'] == 'row':
                columns = len(e['children'])
                e['children'] = fix_column_width(e['children'], columns)
            new_layout.append(e)
        return new_layout

    for obj in get_valid_objects(portal_type='collective.cover.content'):
        try:
            layout = json.loads(obj.cover_layout)
        except TypeError:
            continue  # empty layout?
        layout = fix_column_width(layout)
        obj.cover_layout = json.dumps(layout)

    logger.info('Column widths fixed on collective.cover objects')
