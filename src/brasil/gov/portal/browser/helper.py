# -*- coding: utf-8 -*-
"""Helper view to return the background image used in the site root
when the expandable header is enabled.
"""
from __future__ import absolute_import
from brasil.gov.portal.controlpanel.portal import ISettingsPortal
from plone import api
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.browser import Download
from plone.namedfile.file import NamedImage

import hashlib


class BackgroundImageView(Download):
    """Helper view to return the background image used in the site root
    when the expandable header is enabled.
    """

    def setup(self):
        name = ISettingsPortal.__identifier__ + '.background_image'
        background_image = api.portal.get_registry_record(name, default=None)

        if background_image is None:
            self.data = None
            return

        # set background image data for download
        filename, data = b64decode_file(background_image)
        self.filename = filename
        self.data = NamedImage(data=data, filename=filename)
        self.checksum = hashlib.sha1(data).hexdigest()

    def _getFile(self):
        return self.data

    def __call__(self):
        """Render the background image.

        Make use of HTTP caching headers to decrease server usage:
        image is not cached on browsers and is cached 120 seconds on
        intermediate caches. We use a checksum of the image data as
        ETag to return a 304 (Not Modified) status in case the image
        has not changed since last time it was accessed.

        More information: https://httpwg.org/specs/rfc7234.html
        """
        self.setup()

        if self.data is None:
            # resource no longer available
            self.request.RESPONSE.setStatus(410)  # Gone
            return ''

        # enable image caching for 2 minutes
        self.request.RESPONSE.setHeader('Cache-Control', 'max-age=0, s-maxage=120')
        self.request.RESPONSE.setHeader('ETag', self.checksum)

        match = self.request.get_header('If-None-Match', '')
        if self.checksum == match:
            self.request.response.setStatus(304)  # Not Modified
            return ''

        return super(BackgroundImageView, self).__call__()
