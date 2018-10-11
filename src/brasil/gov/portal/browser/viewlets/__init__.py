# -*- coding: utf-8 -*-
from plone import api
from plone.app.layout.viewlets import ViewletBase


class ErrorReportingViewlet(ViewletBase):
    """A viewlet to display a form for error reporting."""

    def update(self):
        """The viewlet will be available if there is a published
        contact form in the site root called "Relatar erros".
        """
        results = api.content.find(
            depth=1,  # look only on portal root
            id='relatar-erros',
            portal_type='FormFolder',
            review_state='published',
        )
        assert len(results) in (0, 1)  # nosec
        self.available = len(results) == 1

    def render(self):
        if self.available:
            return self.index()
        return u''


class ResourcesViewlet(ViewletBase):
    """This viewlet inserts static resources on page header."""


class CopyrightViewlet(ViewletBase):
    """This viewlet shows the copyright license at the end of the page."""
