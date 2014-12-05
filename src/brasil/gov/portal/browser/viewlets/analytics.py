# -*- coding: utf-8 -*-
from lxml.html import builder as html_builder
from lxml.html import fragments_fromstring as html_fromstring
from lxml.html import tostring as html_tostring
from plone.app.layout.analytics.view import AnalyticsViewlet as AnalyticsViewletBase
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode


class AnalyticsViewlet(AnalyticsViewletBase):
    def render(self):
        """render the webstats snippet adding a div arround it
        """
        ptool = getToolByName(self.context, 'portal_properties')
        snippet = safe_unicode(ptool.site_properties.webstats_js)

        # Putting a div arround the snippets
        div = html_builder.DIV({'id': 'plone-analytics'})  # create the div
        tags = html_fromstring(snippet)  # parse the snippets from html to lxml classes
        div.extend(tags)  # insert the tags into the div
        snippet = safe_unicode(html_tostring(div))  # convert back to string the new tag
        # Putting a div arround the snippets

        return snippet
