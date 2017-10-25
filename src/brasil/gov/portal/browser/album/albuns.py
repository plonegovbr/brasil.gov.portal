# -*- coding: utf-8 -*-
from plone.contentrules import PloneMessageFactory as _
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


class Pagination(object):
    """ Class responsible by pagination
    """

    def __init__(self,
                 context,
                 request,
                 data_type):
        """ Set initial variables and calculate pagination
        """
        self.context = context
        self.request = request
        self.data_type = data_type
        self.params = self.request.form  # pagination get parameters

        # initialize some variables
        self.items_by_page = 9
        self.items_by_line = 3
        self.pages_visible = 7
        self._calc_page_items(int(self.params.get('pagina', 1)))
        # initialize some variables

        self._set_album_attributes()
        self.brains = self._get_brains()
        self.items = self._get_items()

    def _calc_page_items(self, current_page):
        self.current_page = current_page
        self.first_item = (self.current_page - 1) * self.items_by_page
        self.last_item = self.first_item + self.items_by_page

    def _calc_total_items(self, total_items):
        self.total_items = total_items
        fullpage = 1 if self.total_items % self.items_by_page != 0 else 0
        self.total_pages = (self.total_items / self.items_by_page) + fullpage

    def _set_album_attributes(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        # Procuro todas subpastas na pasta do album
        brains = catalog(Type=self.data_type,
                         path={'query': path})
        # Procuro todas subpastas na pasta do album

        for brain in brains:
            item = brain.getObject()
            path = '/'.join(item.getPhysicalPath())
            childs = catalog(Type=['Image', 'Folder'],
                             path={'query': path,
                                   'depth': 1},
                             sort_on='getObjPositionInParent')
            if len(childs) > 0:
                child = childs[0]
                if child.Type == 'Image':
                    if (item.getLayout() != 'galeria_de_fotos'):
                        item.setLayout('galeria_de_fotos')
                        item.reindexObject()
                elif child.Type == 'Folder':
                    if (item.getLayout() != 'galeria_de_albuns'):
                        item.setLayout('galeria_de_albuns')
                        item.reindexObject()

    def _get_brains(self):
        """ Return a list of brains inside the folder
        """
        catalog = getToolByName(self.context, 'portal_catalog')

        # Procuro todas subpastas na pasta do album
        path = '/'.join(self.context.getPhysicalPath())
        brains = catalog(Type=self.data_type,
                         path={'query': path},
                         sort_on='effective',
                         sort_order='reverse',
                         review_state='published')
        # Procuro todas subpastas na pasta do album

        # Retiro as pastas que não são albuns
        albuns = []
        for brain in brains:
            obj = brain.getObject()
            if (obj.getLayout() == 'galeria_de_fotos'):
                albuns.append(brain)
        # Retiro as pastas que não são albuns

        # initialize some variables
        self._calc_total_items(len(albuns))
        # initialize some variables

        return albuns

    def _get_items(self):
        """ Return a list of image objects inside the album
        """
        return [b.getObject() for b in self._get_brains()[self.first_item:self.last_item]]

    def _get_all_pages(self):
        pagination = []
        for i in xrange(1, self.total_pages + 1):
            item = {
                'link': (i != self.current_page),
                'href': '?pagina={0}'.format(i),
                'content': '{0}'.format(i),
                'class': 'atual' if (i == self.current_page) else 'pagina',
                'is_prev': False,
                'is_next': False,
            }
            pagination.append(item)

        return pagination

    def get_pagination(self):
        """ Return a list with the numbers of the images
        """
        pagination = self._get_all_pages()

        if (len(pagination) > self.pages_visible):
            dots = {
                'link': False,
                'href': '',
                'content': '...',
                'class': 'reticencias',
                'is_prev': False,
                'is_next': False,
            }

            limit_start = ((self.pages_visible //
                            2) +
                           2)
            limit_end = (len(pagination) -
                         (self.pages_visible //
                          2) -
                         1)
            if (self.current_page <= limit_start):
                start = 0
                end = self.pages_visible
            elif (self.current_page >= limit_end):
                start = (len(pagination) - self.pages_visible)
                end = len(pagination)
            else:
                start = ((self.current_page - 1) -
                         (self.pages_visible // 2))
                end = ((self.current_page - 1) +
                       (self.pages_visible // 2) +
                       1)
            pagination_visible = pagination[start:end]

            if (pagination_visible[0] != pagination[0]):
                pagination_visible.insert(0, dots)
                pagination_visible.insert(0, pagination[0])
            if (pagination_visible[-1] != pagination[-1]):
                pagination_visible.append(dots)
                pagination_visible.append(pagination[-1])

            pagination = pagination_visible
        # pages

        # prev page
        if (self.current_page > 1):
            item = {
                'link': True,
                'href': '?pagina={0}'.format(self.current_page - 1),
                'content': _(u'label_previous'),
                'class': 'anterior',
                'is_prev': True,
                'is_next': False,
            }
            pagination.insert(0, item)
        # prev page

        # next page
        if (self.current_page < self.total_pages):
            item = {
                'link': True,
                'href': '?pagina={0}'.format(self.current_page + 1),
                'content': _('label_next'),
                'class': 'proximo',
                'is_prev': False,
                'is_next': True,
            }
            pagination.append(item)
        # next page

        return pagination


class GaleriaDeAlbunsView(BrowserView):
    """View de galeria de albuns para pastas."""

    index = ViewPageTemplateFile('templates/galeria_de_albuns.pt')

    def setup(self):
        pagination = Pagination(self.context,
                                self.request,
                                'Folder')
        self.brains = pagination.brains
        self.items = pagination.items
        self.get_pagination = pagination.get_pagination

    def render(self):
        return self.index()

    def __call__(self):
        self.setup()
        return self.render()

    def _toLocalizedTime(self,
                         time,
                         long_format=None,
                         time_only=None):
        plone_view = getMultiAdapter((self.context,
                                      self.request),
                                     name='plone')
        return plone_view.toLocalizedTime(time,
                                          long_format,
                                          time_only)

    def album_total_images(self, item):
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(item.getPhysicalPath())
        brains = catalog(Type='Image',
                         path={'query': path,
                               'depth': 1},
                         sort_on='getObjPositionInParent')
        return len(brains)

    def album_date(self, item):
        return self._toLocalizedTime(item.Date())

    def thumbnail(self, item):
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(item.getPhysicalPath())
        brains = catalog(Type=['Image', 'Folder'],
                         path={'query': path,
                               'depth': 1},
                         sort_on='getObjPositionInParent')
        if len(brains) > 0:
            brain = brains[0]
            if brain.Type == 'Image':
                image = brain.getObject()
                scales = image.restrictedTraverse('@@images')
                thumb = scales.scale('image', 'galeria_de_album_thumb')
                return {
                    'src': thumb.url if thumb else image.absolute_url(),
                    'alt': image.Description(),
                }


class GaleriaDeFotosView(BrowserView):
    """View de galeria de albuns para pastas."""

    index = ViewPageTemplateFile('templates/galeria_de_fotos.pt')

    def setup(self):
        self.items = self._get_items()

    def render(self):
        return self.index()

    def __call__(self):
        self.setup()
        return self.render()

    def _get_brains(self, data_type=None):
        """ Return a list of brains inside the folder
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        brains = catalog(Type=data_type,
                         path={'query': path,
                               'depth': 1},
                         sort_on='getObjPositionInParent')

        return brains

    def _get_items(self):
        """ Return a list of image objects inside the album
        """
        return [{'obj': b.getObject(),
                 'size': b.getObjSize} for b in self._get_brains('Image')]

    def scale(self, item):
        scales = item.restrictedTraverse('@@images')
        scale = scales.scale('image', 'galeria_de_foto_view')
        return scale

    def thumbnail(self, item):
        scales = item.restrictedTraverse('@@images')
        thumb = scales.scale('image', 'galeria_de_foto_thumb')
        return thumb
