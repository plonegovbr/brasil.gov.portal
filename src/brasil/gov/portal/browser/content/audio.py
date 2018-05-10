# -*- coding: utf-8 -*-
from brasil.gov.portal.content.audio_file import IOGGAudioFile
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return '%3.1f %s' % (num, x)
        num /= 1024.0


class AudioView(BrowserView):

    index = ViewPageTemplateFile('templates/audioview.pt')

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def sources(self):
        files = self.context.objectValues()
        return files

    def downloads(self):
        downloads = []
        sources = self.sources()
        for obj in sources:
            format = 'MP3'
            if IOGGAudioFile.providedBy(obj):
                format = 'OGG'
            size = obj.file.size
            downloads.append(
                {'format': format,
                 'size': sizeof_fmt(size),
                 'path': '%s/download' % obj.absolute_url()})
        return downloads
