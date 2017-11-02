# -*- coding: utf-8 -*-
from collective.transmogrifier.interfaces import ISection
from collective.transmogrifier.interfaces import ISectionBlueprint
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from Products.Archetypes.interfaces import IBaseObject
from zope.interface import classProvides
from zope.interface import implements

import base64


class DataFields(object):
    """
    """

    classProvides(ISectionBlueprint)
    implements(ISection)

    def __init__(self, transmogrifier, name, options, previous):
        self.previous = previous
        self.context = transmogrifier.context
        self.datafield_prefix = options.get('datafield-prefix', '_datafield_')
        self.root_path_length = len(self.context.getPhysicalPath())

    def fixattrs(self, item, obj):
        for key in item.keys():
            if not key.startswith(self.datafield_prefix):
                continue
            value = base64.b64decode(item[key]['data'])
            fieldname = key[len(self.datafield_prefix):]
            if IBaseObject.providedBy(obj):
                field = obj.getField(fieldname)
                if field is None:
                    continue
                old_value = field.get(obj).data
                if value != old_value:
                    field.set(obj, value)
                    obj.setFilename(item[key]['filename'])
                    obj.setContentType(item[key]['content_type'])
            else:  # dexterity
                filename = item[key]['filename']
                if fieldname == 'file':
                    wrapped_data = NamedBlobFile(data=value,
                                                 filename=filename)
                elif fieldname == 'image':
                    wrapped_data = NamedBlobImage(data=value,
                                                  filename=filename)
                setattr(obj, fieldname, wrapped_data)

    def __iter__(self):
        for item in self.previous:
            # not enough info
            if '_path' not in item:
                yield item
                continue
            obj = self.context.unrestrictedTraverse(item['_path'].lstrip('/'),
                                                    None)
            # path doesn't exist
            if obj is None:
                yield item
                continue
            # do nothing if we got a wrong object through acquisition
            path = item['_path']
            if path.startswith('/'):
                path = path[1:]
            if '/'.join(obj.getPhysicalPath()[self.root_path_length:]) != path:
                yield item
                continue
            self.fixattrs(item, obj)
            yield item
