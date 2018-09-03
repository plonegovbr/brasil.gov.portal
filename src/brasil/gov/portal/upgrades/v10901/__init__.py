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
            logger.info('Portlet "{0}" removed'.format(i))
            del mapping[i]


def remove_root_portlets(setup_tool):
    """Remove portlet assigments at portal root."""
    logger.info('Removing portlet assigments at portal root')
    remove_portlet_assignments(api.portal.get())
    logger.info('Done')


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

    logger.info('Fixing column widths on collective.cover objects')
    for obj in get_valid_objects(portal_type='collective.cover.content'):
        try:
            layout = json.loads(obj.cover_layout)
        except TypeError:
            continue  # empty layout?
        layout = fix_column_width(layout)
        obj.cover_layout = json.dumps(layout)

    logger.info('Done')


def update_infographic_workflow(setup_tool):
    """Remove workflow from Infographic content type."""
    wftool = api.portal.get_tool('portal_workflow')
    if wftool.getChainForPortalType('Infographic') != ():
        logger.info('Removing workflow from Infographic content type')
        wftool.setChainForPortalTypes(['Infographic'], '')
        logger.info('Done')


def add_content_central_menu(setup_tool):
    """Add Content Central menu option to Folder content type."""
    from brasil.gov.portal.setuphandlers import add_content_central_menu
    add_content_central_menu()
    logger.info('Added Content Central menu option to Folder content type')


def add_results_filter_menu(setup_tool):
    """Add Results Filter menu option to Collection content type."""
    from brasil.gov.portal.setuphandlers import add_results_filter_menu
    add_results_filter_menu()
    logger.info('Added Results Filter menu option to Collection content type')


def uninstall_doormat(setup_tool):
    """Uninstall Products.Doormat.
    The add-on removes itself all related content at uninstall so we
    don't need to do so here.
    """
    addon = 'Doormat'
    qi = api.portal.get_tool('portal_quickinstaller')
    if qi.isProductInstalled(addon):
        qi.uninstallProducts([addon])
        logger.info(addon + ' was uninstalled')


def add_image_sizes(setup_tool):
    """Add image sizes."""
    settings = api.portal.get_tool('portal_properties').imaging_properties
    allowed_sizes = set(settings.allowed_sizes)
    allowed_sizes -= frozenset([u'capa 230:230'])
    allowed_sizes |= frozenset([
        u'Imagem-Full: 1150:1150',
        u'Imagem-8C 760:760',
        u'Imagem-7C 663:663',
        u'Imagem-6C 565:565',
        u'Imagem-5C 468:468',
        u'Imagem-4C 370:370',
        u'Imagem-3C 273:273',
    ])
    settings.allowed_sizes = tuple(allowed_sizes)
    logger.info('Added image sizes.')
