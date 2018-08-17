# -*- coding: utf-8 -*-
from collections import OrderedDict
from DateTime import DateTime
from plone import api
from plone.app.contentlisting.interfaces import IContentListing
from plone.app.search.browser import quote_chars
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView


MEDIA = [
    'sc.embedder',
    'Image',
    'Audio',
    'Infographic',
]

EVER = DateTime(0).Date()


class ContentCentralView(BrowserView):
    """View for media types with filter."""

    def __call__(self):
        self.setup()
        return self.index()

    def setup(self):
        """Hide portlet columns and disable the green bar for
        anonynmous users.
        """
        self.request.set('disable_plone.leftcolumn', True)
        self.request.set('disable_plone.rightcolumn', True)
        if api.user.is_anonymous():
            self.request.set('disable_border', True)

    @staticmethod
    def filter_types(types):
        """Return a list of portal types listed above."""
        if not types:
            return MEDIA

        # respect `types_not_searched` setting
        plone_utils = api.portal.get_tool('plone_utils')
        types = plone_utils.getUserFriendlyTypes(types)
        return [t for t in types if t in MEDIA]

    def results(self, batch=True, b_size=16, b_start=0):
        """Return latests media on the site"""
        query = {
            'sort_on': 'Date',
            'sort_order': 'reverse',
        }
        if batch:
            b_start = int(b_start)

        text = self.request.form.get('SearchableText', '')
        if text:
            query['SearchableText'] = quote_chars(text)

        portal_type = self.request.form.get('portal_type', '')
        portal_type = self.filter_types(portal_type)
        query['portal_type'] = self.filter_types(portal_type)

        created = self.request.form.get('created', {})
        if self.valid_period(created):
            query['created'] = created

        # TODO: include results in current context only
        results = api.content.find(**query)
        results = IContentListing(results)
        if batch:
            results = Batch(results, b_size, b_start)
        return results

    @staticmethod
    def valid_period(period):
        """Check if the selected period is valid."""
        period = period.get('query', [])
        try:
            return period[0].Date() > EVER
        except (AttributeError, IndexError, TypeError):
            return False

    def media(self):
        """Return a list of existing types that can be searched."""
        catalog = api.portal.get_tool('portal_catalog')
        types_tool = api.portal.get_tool('portal_types')
        used_types = catalog._catalog.getIndex('portal_type').uniqueValues()
        used_types = self.filter_types(used_types)
        return OrderedDict([
            (t, types_tool.getTypeInfo(t).Title()) for t in used_types])

    def checked(self):
        """Return the selected period."""
        created = self.request.form.get('created', {})
        created = created.get('query', [])

        try:
            return created[0].Date()
        except (AttributeError, IndexError, TypeError):
            # select EVER if value is not what we expect
            return EVER
