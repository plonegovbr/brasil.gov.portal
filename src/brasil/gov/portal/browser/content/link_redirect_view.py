# -*- coding: utf-8 -*-

from plone.app.contenttypes.browser.link_redirect_view import LinkRedirectView as OriginalView
from plone.app.contenttypes.browser.link_redirect_view import NON_RESOLVABLE_URL_SCHEMES
from plone.app.contenttypes.utils import replace_link_variables_by_paths
from zope.component import getMultiAdapter


class LinkRedirectView(OriginalView):

    def absolute_target_url(self):
        """Compute the absolute target URL."""
        url = self.context.remoteUrl

        if self._url_uses_scheme(NON_RESOLVABLE_URL_SCHEMES):
            # For non http/https url schemes, there is no path to resolve.
            return url

        remote_url_utils = getMultiAdapter(
            (self.context, self.request),
            name=u'remote_url_utils',
        )
        path = '/'.join(self.context.getPhysicalPath())

        if url.startswith('.'):
            # ./ ../ ../../
            url = remote_url_utils.remote_url_transform(
                path,
                url,
            )
        else:
            url = replace_link_variables_by_paths(self.context, url)
            url = remote_url_utils.remote_url_transform(
                path,
                url,
            )
        if not url.startswith(('http://', 'https://')):
            portal_state = self.context.restrictedTraverse(
                '@@plone_portal_state',
            )
            url = '{0}{1}'.format(portal_state.portal_url(), url)

        return url
