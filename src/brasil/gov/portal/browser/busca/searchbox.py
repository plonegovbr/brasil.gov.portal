# -*- coding: utf-8 -*-
"""SearchBoxViewlet customization.

The new search box includes 2 different versions, one similar to the
default but calling @@busca at form submission. The other is an
expandable version that uses information stored in the registry, and
accessible at the @@portal-settings configlet.
"""
from brasil.gov.portal.controlpanel.portal import ISettingsPortal
from plone.app.layout.viewlets.common import SearchBoxViewlet as SearchBoxViewletBase  # noqa: E501
from plone.formwidget.namedfile.converter import b64decode_file
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import mimetypes


class SearchBoxViewlet(SearchBoxViewletBase):
    """Search box viewlet customization."""

    def update(self):
        super(SearchBoxViewlet, self).update()
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISettingsPortal, check=False)
        self.expandable_header = getattr(self.settings, 'expandable_header', False)  # noqa: E501
        self.media_url = self.site_url + '/@@searchbox-background-media'

    @staticmethod
    def split(iterable):
        results = []
        if iterable is None:
            return results

        for item in iterable:
            title, url = item.split('|')
            results.append({'title': title, 'url': url})
        return results

    def featured_news(self):
        """Return the list of defined featured news."""
        return self.split(self.settings.featured_news)

    def more_news(self):
        return self.settings.more_news

    def featured_services(self):
        """Return the list of defined featured services."""
        return self.split(self.settings.featured_services)

    def more_services(self):
        return self.settings.more_services

    def top_subjects(self):
        """Return the list of defined top subjects."""
        return self.split(self.settings.top_subjects)

    def klass(self):
        """Return a CSS class to let Diazo know which search box is in use."""
        if self.expandable_header:
            return 'expandable-header'

    @property
    def is_video(self):
        """Guess if the mimetype of the file stored in the
        background_image field, is from a video.
        """
        if self.settings.background_image is None:
            return False

        filename, _ = b64decode_file(self.settings.background_image)
        self.mimetype, _ = mimetypes.guess_type(filename)
        return 'video' in self.mimetype

    def style(self):
        """Return a CSS style to add a background image to an element.
        If the expandable header is not used, or there is no background
        image defined, return None to remove the style attribute from
        rendering.
        """
        if not self.expandable_header:
            return None

        if self.settings.background_image is None:
            return None

        if self.is_video:
            return None

        return 'background-image: url({0})'.format(self.media_url)
