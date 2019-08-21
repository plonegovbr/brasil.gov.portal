# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from brasil.gov.portal.logger import logger
from plone.app.contenttypes.content import Link
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.outputfilters.filters import resolveuid_and_caption as base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.CMFPlone.browser.navigation import get_id
from Products.CMFPlone.browser.navigation import get_view_url
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


def topLevelTabs(self, actions=None, category='portal_tabs'):
    """
    Esse método veio de

        https://github.com/plone/Products.CMFPlone/blob/4.3.18/Products/CMFPlone/browser/navigation.py

    Com o objetivo de alterar o comportamento de get_link_url:

        https://github.com/plone/Products.CMFPlone/blob/4.3.18/Products/CMFPlone/browser/navigation.py#L195

    É a única customização no método topLevelTabs.

    Em tese, poderia ter sido feito um patch apenas no método get_link_url, mas
    como o formato é uma função de uma função e a documentação de como isso deve
    ser feito consideramos complexa:

        https://stackoverflow.com/questions/27550228/can-you-patch-just-a-nested-function-with-closure-or-must-the-whole-outer-fun/27550237

    Decidimos ir pelo caminho de copiar a topLevelTabs.
    """
    context = aq_inner(self.context)

    mtool = getToolByName(context, 'portal_membership')
    member = mtool.getAuthenticatedMember().id

    portal_properties = getToolByName(context, 'portal_properties')
    self.navtree_properties = getattr(portal_properties,
                                      'navtree_properties')
    self.site_properties = getattr(portal_properties,
                                   'site_properties')
    self.portal_catalog = getToolByName(context, 'portal_catalog')

    if actions is None:
        context_state = getMultiAdapter((context, self.request),
                                        name=u'plone_context_state')
        actions = context_state.actions(category)

    # Build result dict
    result = []
    # first the actions
    if actions is not None:
        for actionInfo in actions:
            data = actionInfo.copy()
            data['name'] = data['title']
            result.append(data)

    # check whether we only want actions
    if self.site_properties.getProperty('disable_folder_sections', False):
        return result

    query = self._getNavQuery()

    rawresult = self.portal_catalog.searchResults(query)

    def get_link_url(item):
        linkremote = item.getRemoteUrl and not member == item.Creator  # NOQA
        if linkremote:
            # patch: Substitui o path pela url do site.
            remote_url_utils = getMultiAdapter(
                (item, item.REQUEST),
                name=u'remote_url_utils',
            )
            remote_url = item.getRemoteUrl and item.getRemoteUrl or None
            remote_url_transform = remote_url_utils.remote_url_transform(
                item.getPath(),
                remote_url,
            )
            return (get_id(item), remote_url_transform)
            # patch
        else:
            return False

    # now add the content to results
    idsNotToList = self.navtree_properties.getProperty('idsNotToList', ())
    for item in rawresult:
        if not (item.getId in idsNotToList or item.exclude_from_nav):
            id, item_url = get_link_url(item) or get_view_url(item)
            data = {'name': utils.pretty_title_or_id(context, item),
                    'id': item.getId,
                    'url': item_url,
                    'description': item.Description}
            result.append(data)

    return result


def run():
    outputfilters()
    link()
