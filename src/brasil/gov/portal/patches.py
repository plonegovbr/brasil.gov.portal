# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from brasil.gov.portal.logger import logger
from plone.app.contenttypes.content import Link
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.outputfilters.filters import resolveuid_and_caption as base
from Products.CMFPlone import utils
from zope.component import getMultiAdapter
from zope.component import queryUtility


def outputfilters():
    def patched_call(self, data):
        """ Patch original __call__ """
        data = data.replace('/>', ' />')
        return self.__orig_call__(data)

    setattr(base.ResolveUIDAndCaptionFilter,
            '__orig_call__',
            base.ResolveUIDAndCaptionFilter.__call__)

    setattr(base.ResolveUIDAndCaptionFilter,
            '__call__',
            patched_call)
    logger.info('Patched ResolveUIDAndCaptionFilter')


def link():
    def getRemoteUrl(self):
        return self.remoteUrl

    setattr(Link,
            'getRemoteUrl',
            getRemoteUrl)
    logger.info('Patched Link content type')


# XXXX: this patch should be removed when this is fixed:
#       https://github.com/zopefoundation/z3c.form/pull/76
def deselect(self):
    selecteditems = []
    notselecteditems = []
    for selecteditem in self.selectedItems:
        selecteditems.append(selecteditem['value'])
    for item in self.items:
        if not item['value'] in selecteditems:
            notselecteditems.append(item)
    return notselecteditems


# XXXX: this patch should be removed when this is fixed:
#       https://github.com/collective/collective.recaptcha/pull/18/files
def image_tag(self):
    if not self.settings.public_key:
        raise ValueError(
            'Chave pública do recaptcha não está configurada. '  # noqa
            'Va para /@@recaptcha-settings para configurar.'  # noqa
        )
    return self._old_image_tag()


def decoratorFactory(self, node):
    """Substituicao do path pela url do site ao utilizar o metadado getRemoteUrl
       obtido via portal_catalog.
       Demanda PR para correção da issue 463:
       https://github.com/plonegovbr/brasil.gov.portal/issues/463
    """
    context = aq_inner(self.context)
    request = context.REQUEST

    newNode = node.copy()
    item = node['item']

    portalType = getattr(item, 'portal_type', None)
    itemUrl = item.getURL()
    if portalType is not None and portalType in self.viewActionTypes:
        itemUrl += '/view'

    useRemoteUrl = False
    getRemoteUrl = getattr(item, 'getRemoteUrl', None)
    isCreator = self.memberId == getattr(item, 'Creator', None)
    if getRemoteUrl and not isCreator:
        useRemoteUrl = True

    isFolderish = getattr(item, 'is_folderish', None)
    showChildren = False
    if isFolderish and \
            (portalType is None or portalType not in self.parentTypesNQ):
        showChildren = True

    ploneview = getMultiAdapter((context, request), name=u'plone')

    newNode['Title'] = utils.pretty_title_or_id(context, item)
    newNode['id'] = item.getId
    newNode['UID'] = item.UID
    newNode['absolute_url'] = itemUrl
    newNode['getURL'] = itemUrl
    newNode['path'] = item.getPath()
    newNode['item_icon'] = ploneview.getIcon(item)
    newNode['Creator'] = getattr(item, 'Creator', None)
    newNode['creation_date'] = getattr(item, 'CreationDate', None)
    newNode['portal_type'] = portalType
    newNode['review_state'] = getattr(item, 'review_state', None)
    newNode['Description'] = getattr(item, 'Description', None)
    newNode['show_children'] = showChildren
    newNode['no_display'] = False  # We sort this out with the nodeFilter
    # BBB getRemoteUrl and link_remote are deprecated, remove in Plone 4
    # patch: Substitui o path pela url do site.
    remote_url_utils = getMultiAdapter(
        (context, request),
        name=u'remote_url_utils',
    )
    remote_url = item.getRemoteUrl and item.getRemoteUrl or None
    newNode['getRemoteUrl'] = remote_url_utils.remote_url_transform(
        newNode['path'],
        remote_url,
    )
    # patch
    newNode['useRemoteUrl'] = useRemoteUrl
    newNode['link_remote'] = newNode['getRemoteUrl'] \
        and newNode['Creator'] != self.memberId

    idnormalizer = queryUtility(IIDNormalizer)
    newNode['normalized_portal_type'] = idnormalizer.normalize(portalType)
    newNode['normalized_review_state'] = \
        idnormalizer.normalize(newNode['review_state'])
    newNode['normalized_id'] = idnormalizer.normalize(newNode['id'])

    return newNode

    logger.info('Patched Products.CMFPlone.browser.navtree.SitemapNavtreeStrategy:decoratorFactory:191')


def run():
    outputfilters()
    link()
