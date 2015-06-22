# -*- coding: utf-8 -*-
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from collective.transmogrifier.utils import resolvePackageReferenceOrFile
from zope.interface import classProvides
from zope.interface import implements

import json
import os


class JSONSourceSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.directory = self.resolve_directory(options['directory'])

    def resolve_directory(self, value):
        if value.startswith('$'):
            directory = os.getenv(value[1:], '')
        else:
            directory = resolvePackageReferenceOrFile(value)
        return directory

    def read_directory(self, directory):
        data_file = 'data.json'
        children_file = 'children.json'
        try:
            path = '%s/%s' % (directory, data_file)
            data = json.loads(open(path, 'r').read())
        except Exception:
            data = {}

        yield data

        try:
            children = json.loads(open('%s/%s' % (directory, children_file),
                                       'r').read())
        except Exception:
            children = []
        for child in children:
            oId = child.get('id')
            path = '%s/%s' % (directory, oId)
            for item in self.read_directory(path):
                yield item

    def __iter__(self):
        for item in self.previous:
            yield item

        path = self.directory
        for item in self.read_directory(path):
            if not item:
                continue
            item['creators'] = u'Brasil'
            yield item
