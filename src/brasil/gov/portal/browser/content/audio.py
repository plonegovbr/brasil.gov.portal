# -*- coding: utf-8 -*-
from brasil.gov.portal.content.audio import IAudio
from brasil.gov.portal.content.audio_file import IOGGAudioFile
from five import grok

grok.templatedir('templates')


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return '%3.1f %s' % (num, x)
        num /= 1024.0


class AudioView(grok.View):
    grok.context(IAudio)
    grok.name('view')

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
                 'path': '%s/download' % obj.absolute_url()}
            )
        return downloads
