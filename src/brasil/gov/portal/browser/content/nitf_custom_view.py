# -*- coding: utf-8 -*-

from collective.nitf.browser import View as NITFView
from five import grok
from secom.brasil.portal.interfaces import IBrasilGov

grok.templatedir('templates')


class View(NITFView):
    """Customize NITF view
    """
    grok.layer(IBrasilGov)
    grok.name('nitf_custom_view')
    grok.template('nitf_custom_view')

    def show_more_images(self):
        return len(self.get_images()) > 1

    def get_link_erros(self):
        portal_obj = self.context.portal_url.getPortalObject()
        if (hasattr(portal_obj, 'relatar-erros')):
            return self.context.absolute_url() + '/relatar-erros'
        else:
            return None
