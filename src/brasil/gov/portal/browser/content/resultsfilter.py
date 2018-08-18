# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone import api
from plone.app.search.browser import quote_chars
from Products.Five.browser import BrowserView


EVER = DateTime(0).Date()


class ResultsFilterView(BrowserView):
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

    def results(self, b_size=5, b_start=0):
        """Apply a custom query over the collection results."""
        custom_query = {}
        b_start = int(b_start)

        text = self.request.form.get('SearchableText', '')
        if text:
            custom_query['SearchableText'] = quote_chars(text)

        created = self.request.form.get('created', {})
        if self.valid_period(created):
            custom_query['created'] = created

        sort_on = self.request.form.get('sort_on', '')
        if sort_on not in ('', 'Date', 'sortable_title'):
            sort_on = ''
        sort_order = 'reverse' if sort_on == 'Date' else 'ascending'
        custom_query['sort_order'] = sort_order

        results = self.context.results(
            b_start=b_start,
            b_size=b_size,
            custom_query=custom_query,
            sort_on=sort_on,
        )
        return results

    @staticmethod
    def valid_period(period):
        period = period.get('query', [])
        try:
            return period[0].Date() > EVER
        except (AttributeError, IndexError, TypeError):
            return False

    def checked(self):
        """Return the selected period."""
        created = self.request.form.get('created', {})
        created = created.get('query', [])

        try:
            return created[0].Date()
        except (AttributeError, IndexError, TypeError):
            # select EVER if value is not what we expect
            return EVER
