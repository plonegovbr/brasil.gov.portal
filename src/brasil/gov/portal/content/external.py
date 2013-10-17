    # -*- coding: utf-8 -*-
from five import grok
from plone.dexterity.content import Item
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.interface import Interface


grok.templatedir('templates')


def has_image(blog_entry):
    image = blog_entry.image
    return (image and image.getSize())


class IExternalContent(Interface):
    """ Um conteudo externo a este site
    """


class ExternalContent(Item):
    implements(IExternalContent)

    def image_thumb(self):
        ''' Return a thumbnail '''
        if not has_image(self):
            return None
        view = self.unrestrictedTraverse('@@images')
        return view.scale(fieldname='image',
                          scale='thumb').index_html()

    def tag(self, scale='thumb', css_class='tileImage', **kw):
        ''' Return a tag to the image '''
        if not (has_image(self)):
            return ''
        view = self.unrestrictedTraverse('@@images')
        return view.tag(fieldname='image',
                        scale=scale,
                        css_class=css_class,
                        **kw)


class ExternalContentView(grok.View):
    grok.context(IExternalContent)
    grok.name('view')

    def update(self):
        """Redireciona usuarios sem poder de edicao para o conteudo externo"""
        context = self.context
        mtool = getToolByName(context, 'portal_membership')

        can_edit = mtool.checkPermission('Modify portal content', context)

        if not can_edit:
            url = context.remoteUrl
            return context.REQUEST.RESPONSE.redirect(url)
