# -*- coding: utf-8 -*-

from plone.app.contenttypes.browser.link_redirect_view import NON_RESOLVABLE_URL_SCHEMES
from Products.Five import BrowserView
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.interface import Interface


class IRemoteUrlUtils(Interface):

    def _url_uses_scheme(self):
        """"""

    def remote_url_transform(self):
        """Transforma o path em url do site."""


class RemoteUrlUtils(BrowserView):
    """
    Substituicao do path pela url do site.
    Utilizado para o tratamento do valor obtido do metadado getRemoteUrl
    via portal_catalog e pela visao padrao do tipo Link (link_redirect_view).
    Demanda PR para correção da issue 463:
    https://github.com/plonegovbr/brasil.gov.portal/issues/463
    """
    implements(IRemoteUrlUtils)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state',
        )
        self.portal_path = self.portal_state.navigation_root_path()
        self.portal_url = self.portal_state.portal_url()

    def _url_uses_scheme(self, url=None):
            for scheme in NON_RESOLVABLE_URL_SCHEMES:
                if url.startswith(scheme):
                    return True
            return False

    def remote_url_transform(self, path=None, url=None):
        """Transforma o path em url do site."""
        if url:
            # http:// https://
            if url.startswith('http://') or url.startswith('https://'):
                return url
            # file: ftp: mailto: webdav: ...
            if self._url_uses_scheme(url):
                return url
            # ./ ../
            if path:
                if url.startswith('.'):
                    path_items = path.split('/')
                    url_items = url.split('/')
                    # ./
                    if url_items[0] == '.':
                        url = url.replace(
                            './',
                            '/'.join(path_items[:-1]) + '/',
                        )
                    # ../  ../../../
                    elif url_items[0] == '..':
                        count = url.count('../')
                        position = count + 1
                        url = url.replace(
                            '../' * count,
                            '/'.join(path_items[:-position]) + '/',
                        )
            # /path/site
            url = url.replace(self.portal_path, self.portal_url)
        return url
