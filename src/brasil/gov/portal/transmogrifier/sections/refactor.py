# -*- coding: utf-8 -*-
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from plone.namedfile.file import NamedBlobImage
from plone.tiles.interfaces import ITileDataManager
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.interface import classProvides
from zope.interface import implements
from zope.intid.interfaces import IIntIds

import base64


class RefactorSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous

    def __iter__(self):
        for item in self.previous:
            self.transmogrify(item)
            yield item

    def transmogrify(self, item):
        pt = item['_type']
        # Fix path
        item['_path'] = str(item['_path'])
        # Default page
        if pt not in ('Folder', 'Collection') and '_defaultpage' in item:
            del(item['_defaultpage'])
        if pt in ('File', 'Image', 'Document', 'News Item'):
            item['description'] = item.get('description', '')
        # VCGE
        if not item.get('skos'):
            item['skos'] = []


class UpdateCoverSection(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context

    def __iter__(self):
        for item in self.previous:
            self.transmogrify(item)
            yield item

    def transmogrify(self, item):
        if item['_type'] == 'collective.cover.content':
            path = item['_path']
            if path.startswith('/'):
                path = path[1:]
            cover = self.context.restrictedTraverse(str(path))
            tiles = item['tile_data']
            for tile_id, tile_info in tiles.items():
                tile_data = tile_info['data']
                tile_config = tile_info['config']
                tile = cover.restrictedTraverse(str(tile_id))
                tile.set_tile_configuration(tile_config)
                if tile_data.get('image', None):
                    value = base64.b64decode(tile_data['image']['data'])
                    filename = tile_data['image']['filename']
                    wrapped_data = NamedBlobImage(data=value,
                                                  filename=filename)
                    tile_data['image'] = wrapped_data
                data_mgr = ITileDataManager(tile)
                data_mgr.set(tile_data)


class RelatedItems(object):
    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        self.to_fix = []

    def __iter__(self):
        for item in self.previous:
            if item.get('_data_relatedItems', ''):
                to_fix = self.to_fix
                to_fix.append((item['_path'], item['_data_relatedItems']))
                self.to_fix = to_fix
            yield item

        intids = getUtility(IIntIds)
        for path, refs in self.to_fix:
            relatedItems = []
            try:
                o = self.context.restrictedTraverse(str(path))
            except KeyError:
                continue
            for ref in refs:
                oRef = self.context.restrictedTraverse(ref)
                to_id = intids.getId(oRef)
                relatedItems.append(RelationValue(to_id))
            o.relatedItems = relatedItems
