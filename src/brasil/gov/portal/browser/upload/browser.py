# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.ATContentTypes.interfaces import IATFile
from Products.ATContentTypes.interfaces import IATImage
from Products.CMFPlone.utils import safe_unicode
from collective.upload import browser
from collective.upload.config import IMAGE_MIMETYPES
from collective.upload.interfaces import IUploadBrowserLayer
from five import grok
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from zope.component import queryMultiAdapter
from zope.container.interfaces import INameChooser
from zope.event import notify
from zope.interface import Interface
from zope.lifecycleevent import ObjectModifiedEvent


grok.templatedir('templates')


class Media_Uploader(browser.Media_Uploader):
    grok.context(Interface)
    grok.require('collective.upload.UploadFiles')

    def __call__(self, *args, **kwargs):
        if hasattr(self.request, 'REQUEST_METHOD'):
            json_view = queryMultiAdapter((self.context, self.request),
                                          name=u'api')
            if self.request['REQUEST_METHOD'] == 'POST':
                if getattr(self.request, 'files[]', None) is not None:
                    files = self.request['files[]']
                    title = self.request['title[]']
                    description = self.request['description[]']
                    rights = self.request['rights[]']
                    uploaded = self.upload([files], [title], [description], [rights])
                    if uploaded and json_view:
                        upped = []
                        for item in uploaded:
                            upped.append(json_view.getContextInfo(item))
                        return json_view.dumps(upped)
                return json_view()
        return super(Media_Uploader, self).__call__(*args, **kwargs)

    def _create_file(self, item, files, title, description, rights):
        namechooser = INameChooser(self.context)
        content_type = item.headers.get('Content-Type')
        filename = safe_unicode(item.filename)
        data = item.read()
        id_name = ''
        title = title and title[0] or filename
        id_name = namechooser.chooseName(title, self.context)

        if content_type in IMAGE_MIMETYPES:
            portal_type = 'Image'
            wrapped_data = NamedBlobImage(data=data, filename=filename)
        else:
            portal_type = 'File'
            wrapped_data = NamedBlobFile(data=data, filename=filename)

        self.context.invokeFactory(portal_type,
                                   id=id_name,
                                   title=title,
                                   description=description[0],
                                   rights=rights[0])
        newfile = self.context[id_name]
        if portal_type == 'File':
            if IATFile.providedBy(newfile):
                newfile.setFile(data, filename=filename)
            else:
                newfile.file = wrapped_data
        elif portal_type == 'Image':
            if IATImage.providedBy(newfile):
                newfile.setImage(data, filename=filename)
            else:
                newfile.image = wrapped_data
        newfile.reindexObject()
        notify(ObjectModifiedEvent(newfile))
        return newfile

    def upload(self, files, title='', description='', rights=''):
        loaded = []
        if not isinstance(files, list):
            files = [files]
        for item in files:
            if item.filename:
                newfile = self._create_file(item, files, title, description, rights)
                loaded.append(newfile)
        if loaded:
            return loaded
        return False


class JSON_View(browser.JSON_View):
    grok.context(Interface)
    grok.name('api')
    grok.require('cmf.AddPortalContent')
    grok.layer(IUploadBrowserLayer)

    json_var = {'name': 'File-Name.jpg',
                'title': '',
                'description': '',
                'rights': '',
                'size': 999999,
                'url': '\/\/nohost.org',
                'thumbnail_url': '//nohost.org',
                'delete_url': '//nohost.org',
                'delete_type': 'DELETE',
                }

    def getContextInfo(self, context=None):
        if context is None:
            context = self.context
        context = aq_inner(context)

        info = ''
        context_name = context.Title()
        context_url = context.absolute_url()
        context_type = context.Type()
        del_url = context_url

        info = {'name': context_name,
                'title': context_name,
                'description': context.Description(),
                'rights': context.Rights(),
                'url': context_url,
                'delete_url': del_url,
                'delete_type': 'DELETE',
                }
        if hasattr(context, 'size'):
            info['size'] = context.size()
        else:
            if context_type == 'File':
                info['size'] = context.file.getSize()
            elif context_type == 'Image':
                info['size'] = context.image.getSize()
        if context_type == 'Image':
            scales = context.restrictedTraverse('@@images')
            thumb = scales.scale(fieldname='image', scale='thumb')
            info['thumbnail_url'] = thumb.url
        return info
