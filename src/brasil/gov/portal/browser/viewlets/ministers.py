# -*- coding: utf-8 -*-
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from random import shuffle


def catalog_counter_cachekey(method, self):
    """Return a cachekey based on catalog updates."""
    catalog = api.portal.get_tool('portal_catalog')
    return str(catalog.getCounter())


class MinistersViewlet(ViewletBase):
    """A viewlet to display a gallery of Ministers."""

    @property
    def available(self):
        """Show the viewlet on the default view only."""
        return self.request['PUBLISHED'].__name__ == 'view'

    def render(self):
        if not self.available:
            return ''
        return self.index()

    @property
    def ministers(self):
        # get all ministries except the current one
        ministries = api.content.find(portal_type='Ministry')
        ministries = [
            m.getObject() for m in ministries
            if m.UID != self.context.UID()]

        # get the information from the ministries
        ministers = []
        for m in ministries:
            ministers.append({
                'minister': m.minister,
                'ministry': m.title,
                'scales': m.restrictedTraverse('images'),
                'url': m.absolute_url(),
            })
        shuffle(ministers)  # randomize the list
        return ministers

    def chunks(self, n):
        """Yield successive n-sized chunks from a sequence.
        https://stackoverflow.com/a/312464
        """
        ministers = self.ministers
        for i in range(0, len(ministers), n):
            yield ministers[i:i + n]
