# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from collective.nitf.upgrades.v2000 import get_valid_objects
from plone import api

import transaction


def reindex_get_remote_url_link(setup_tool):
    """
    Reindexa Link para corrigir ${portal_url} e ${navigation_root_url} que não
    foram reindexados após atualização de plone.app.contenttypes 1.0 para 1.1.x.
    """
    logger.info('Reindexing the catalog: getRemoteUrl of Link type.')
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog(portal_type='Link')
    logger.info(u'Found {0} Links.'.format(len(results)))
    for n, obj in enumerate(get_valid_objects(results), start=1):
        # catalog.catalog_object(obj, idxs=['getRemoteUrl'])
        # lança KeyError: 'getRemoteUrl'. Use catalog.indexes() para ver os
        # índices disponíveis.
        catalog.catalog_object(obj)
        if n % 1000 == 0:
            transaction.commit()
            logger.info('{0} items processed.'.format(n))

    transaction.commit()
    logger.info('Done.')
