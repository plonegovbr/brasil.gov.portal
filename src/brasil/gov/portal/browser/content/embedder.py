# -*- coding: utf-8 -*-
from five import grok
from sc.embedder.content.embedder import IEmbedder

grok.templatedir('templates')


class View(grok.View):
    grok.context(IEmbedder)
    grok.require('zope2.View')
    grok.name('view')
    grok.template('embedder_custom_view')

    def get_player_pos_class(self):
        """ Returns the css class based on the position of the embed item.
        """
        pos = self.context.player_position
        css_class = '%s_embedded' % pos.lower()
        return css_class
