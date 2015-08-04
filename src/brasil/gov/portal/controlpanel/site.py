# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode
from brasil.gov.portal import _ as _
from plone import api
from plone.app.controlpanel.form import ControlPanelForm
from zope.component import adapts
from zope.formlib import form
from zope.formlib.textwidgets import TextAreaWidget
from zope.interface import Interface
from zope.interface import implements
from zope.schema import Bool
from zope.schema import SourceText
from zope.schema import Text
from zope.schema import TextLine


class ISiteSchema(Interface):

    site_title_1 = TextLine(
        title=_(u'Site title (First Line)'),
        description=_(u'First line of site title'),
        required=False,
        default=u'')

    site_title_2 = TextLine(
        title=_(u'Site title (Second Line)'),
        description=_(u'Second line of site title'),
        default=u'')

    site_orgao = TextLine(
        title=_(u'Department'),
        description=_(u'Name of Ministry or Department '
                      u'to which this site is subject.'),
        required=False,
        default=u'')

    url_orgao = TextLine(
        title=_(u'Url ID of Department'),
        description=_(u'Url ID for Ministry or Department to which this site is subject.'),
        required=False,
        default=u'')

    site_description = Text(
        title=_(u'Site description'),
        description=_(u'The site description is available '
                      u'in syndicated content and in search engines. '
                      u'Keep it brief.'),
        default=u'',
        required=False)

    exposeDCMetaTags = Bool(
        title=_(u'Expose Dublin Core metadata'),
        description=_(u'Exposes the Dublin Core properties as metatags.'),
        default=False,
        required=False)

    display_pub_date_in_byline = Bool(
        title=_(u'Display publication date in about information'),
        description=_(u'Displays content publication date on site pages.'),
        default=False,
        required=False)

    enable_sitemap = Bool(
        title=_(u'Expose sitemap.xml.gz'),
        description=_(u'Exposes your content as a file '
                      u'according to the sitemaps.org standard. You '
                      u'can submit this to compliant search engines '
                      u'like Google, Yahoo and Microsoft. It allows '
                      u'these search engines to more intelligently '
                      u'crawl your site.'),
        default=False,
        required=False)

    webstats_js = SourceText(
        title=_(u'JavaScript for web statistics support'),
        description=_(u'For enabling web statistics support '
                      u'from external providers (for e.g. Google '
                      u'Analytics). Paste the code snippets provided. '
                      u'It will be included in the rendered HTML as '
                      u'entered near the end of the page.'),
        default=u'',
        required=False)


class SiteControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(ISiteSchema)

    def __init__(self, context):
        super(SiteControlPanelAdapter, self).__init__(context)
        self.portal = api.portal.get()
        self.pprop = getToolByName(context, 'portal_properties')
        self.context = self.pprop.site_properties
        self.encoding = self.pprop.site_properties.default_charset

    def get_site_title(self):
        title = getattr(self.portal, 'title', u'')
        return safe_unicode(title)

    def set_site_title(self, value):
        pass

    def get_site_title_1(self):
        title = getattr(self.portal, 'title_1', u'')
        return safe_unicode(title)

    def set_site_title_1(self, value):
        value = value or ''
        self.portal.title_1 = value.encode(self.encoding)
        title_1 = safe_unicode(self.portal.title_1)
        title_2 = safe_unicode(self.portal.title_2)
        title = u'%s %s' % (title_1, title_2)
        self.portal.title = title.encode(self.encoding)

    def get_site_title_2(self):
        title = getattr(self.portal, 'title_2', u'')
        return safe_unicode(title)

    def set_site_title_2(self, value):
        value = value or ''
        self.portal.title_2 = value.encode(self.encoding)
        title_1 = safe_unicode(self.portal.title_1)
        title_2 = safe_unicode(self.portal.title_2)
        title = u'%s %s' % (title_1, title_2)
        self.portal.title = title.encode(self.encoding)

    def get_site_orgao(self):
        orgao = getattr(self.portal, 'orgao', u'')
        return safe_unicode(orgao)

    def set_site_orgao(self, value):
        value = value or ''
        self.portal.orgao = value.encode(self.encoding)

    def get_url_orgao(self):
        # Define que o contexto a ser utilizado
        # sera a property sheet brasil_gov
        configs = getattr(self.pprop, 'brasil_gov', None)
        url_orgao = configs.getProperty('url_orgao', u'')
        return safe_unicode(url_orgao)

    def set_url_orgao(self, value):
        value = value or ''
        # Define que o contexto a ser utilizado
        # sera a property sheet brasil_gov
        configs = getattr(self.pprop, 'brasil_gov', None)
        configs.manage_changeProperties(url_orgao=value)

    def get_site_description(self):
        description = getattr(self.portal, 'description', u'')
        return safe_unicode(description)

    def set_site_description(self, value):
        if value is not None:
            self.portal.description = value.encode(self.encoding)
        else:
            self.portal.description = ''

    def get_webstats_js(self):
        description = getattr(self.context, 'webstats_js', u'')
        return safe_unicode(description)

    def set_webstats_js(self, value):
        if value is not None:
            self.context.webstats_js = value.encode(self.encoding)
        else:
            self.context.webstats_js = ''

    site_title = property(get_site_title, set_site_title)
    site_title_1 = property(get_site_title_1, set_site_title_1)
    site_title_2 = property(get_site_title_2, set_site_title_2)
    site_orgao = property(get_site_orgao, set_site_orgao)
    url_orgao = property(get_url_orgao, set_url_orgao)
    site_description = property(get_site_description, set_site_description)
    webstats_js = property(get_webstats_js, set_webstats_js)

    enable_sitemap = ProxyFieldProperty(ISiteSchema['enable_sitemap'])
    exposeDCMetaTags = ProxyFieldProperty(ISiteSchema['exposeDCMetaTags'])

    def get_display_pub_date_in_byline(self):
        return self.context.site_properties.displayPublicationDateInByline

    def set_display_pub_date_in_byline(self, value):
        self.context.site_properties.displayPublicationDateInByline = value

    display_pub_date_in_byline = property(get_display_pub_date_in_byline,
                                          set_display_pub_date_in_byline)


class MiniTextAreaWidget(TextAreaWidget):

    height = 3


class SmallTextAreaWidget(TextAreaWidget):

    height = 5


class SiteControlPanel(ControlPanelForm):

    form_fields = form.FormFields(ISiteSchema)
    form_fields['site_description'].custom_widget = MiniTextAreaWidget
    form_fields['webstats_js'].custom_widget = SmallTextAreaWidget

    label = _('Site settings')
    description = _('Site-wide settings.')
    form_name = _('Site settings')
