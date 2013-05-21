# -*- coding:utf-8 -*-
from brasil.gov.portal.content.audio import IAudio
from five import grok

grok.templatedir('templates')


class AudioView(grok.View):
    grok.context(IAudio)
    grok.name('view')

    def sources(self):
        files = self.context.objectValues()
        return files
