# -*- coding: utf-8 -*-
from brasil.gov.portal import _
from plone import api
from plone.app.registry.browser import controlpanel
from plone.i18n.normalizer import idnormalizer
from plone.memoize.view import memoize
from Products.CMFCore.ActionInformation import Action
from Products.CMFCore.ActionInformation import ActionCategory
from Products.CMFCore.interfaces import IAction
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema
from zope.interface import Interface

import re
import time
import z3c.form.interfaces


ACTION_CATEGORY = 'portal_services'


class IPortalServicesSettings(Interface):
    """Campos dos formulários de inserção e edição do Configlet."""

    pid = schema.TextLine(
        title=_(u'id'),
        required=False,
    )

    title = schema.TextLine(
        title=_(u'Titulo do link'),
        required=True,
    )

    description = schema.Text(
        title=_(u'Description'),
        description=_(u'Informe a descrição caso seja necessário.'),
        required=False,
    )

    url_expr = schema.TextLine(
        title=_(u'URL'),
        description=_(u'Informe o caminho relativo ao portal e começando com uma barra "/" e '
                      u'para URL externa informe http:// ou https://.'),
        required=True,
    )

    visible = schema.Bool(
        title=_(u'Visível'),
        description=_(u'Desmarque para ocultar o link.'),
        default=True,
    )


def get_category():
    """Obtem a categoria do portal_actions"""
    portal_actions = api.portal.get_tool(name='portal_actions')
    category = portal_actions.get(ACTION_CATEGORY, None)
    if not category:
        portal_actions._setObject(ACTION_CATEGORY, ActionCategory(ACTION_CATEGORY))
        return get_category()
    return category


def url_expression(url):
    """Insere a expressão apropriada para a url"""
    if url.find('/') == 0:
        return 'string:${globals_view/navigationRootUrl}%s' % url
    elif url.find('string:') == 0:
        return url
    elif re.compile('^(ht|f)tps?\:', re.I).search(url):
        return 'string:%s' % url
    else:
        return 'string:${portal_url}/%s' % url


class PortalServicesSettings(BrowserView):
    """Configlet gereciador dos links adicionados."""

    template = ViewPageTemplateFile('portalservices.pt')

    def __call__(self):

        form = self.request.form

        if form.get('pid', False):

            if form.get('form.button.delete', None) is not None:
                pid = form.get('pid', None)
                if self.delete_item(pid):
                    api.portal.show_message(
                        message=_(u'Item deleted.'), request=self.request)
                else:
                    api.portal.show_message(
                        message=_(u'Item not deleted.'), request=self.request)

            elif form.get('form.button.moveup', None) is not None:
                pid = form.get('pid', None)
                if self.move_item(pid, 'move_up'):
                    api.portal.show_message(
                        message=_(u'Item moved.'), request=self.request)
                else:
                    api.portal.show_message(
                        message=_(u'Item not moved.'), request=self.request)

            elif form.get('form.button.movedown', None) is not None:
                pid = form.get('pid', None)
                if self.move_item(pid, 'move_down'):
                    api.portal.show_message(
                        message=_(u'Item moved.'), request=self.request)
                else:
                    api.portal.show_message(
                        message=_(u'Item not moved.'), request=self.request)

        return self.template()

    @memoize
    def get_items(self):
        items = []
        for item in get_category().objectValues():
            if IAction.providedBy(item):
                items.append(item)
        return items

    def delete_item(self, pid):
        portal_tabs = get_category()
        portal_tabs.manage_delObjects(ids=[pid])
        return True

    def move_item(self, pid, op):
        portal_tabs = get_category()
        if op == 'move_up':
            portal_tabs.moveObjectsUp([pid], 1)
        else:
            portal_tabs.moveObjectsDown([pid], 1)
        return True


class PortalServicesAddForm(form.AddForm):
    """Formulário de adicição de action no portal_actions."""

    label = _(u'Add a link.')
    fields = field.Fields(IPortalServicesSettings)

    def updateWidgets(self):
        super(PortalServicesAddForm, self).updateWidgets()
        self.widgets['pid'].mode = z3c.form.interfaces.HIDDEN_MODE
        self.widgets['visible'].mode = z3c.form.interfaces.HIDDEN_MODE

    def create(self, data):

        id = idnormalizer.normalize(data['title'])
        id += '-' + str(int(time.time()))

        data.pop('pid')
        data['title'] = data['title']
        if data['description']:
            data['description'] = data['description']
        else:
            data['description'] = ''
        data['i18n_domain'] = 'plone'
        data['permissions'] = ('View',)
        data['visible'] = True
        data['url_expr'] = url_expression(data.get('url_expr'))

        action = Action(id, **data)
        return action

    def add(self, action):
        category = get_category()
        category._setObject(action.id, action)
        self.status = _(u'Item added successfully.')

    def nextURL(self):
        url = self.context.absolute_url()
        url += '/@@portal-services-settings'
        return url


class PortalServicesAddFormPageWrapper(controlpanel.ControlPanelFormWrapper):
    """Página de configuração do Portal Padrão"""
    form = PortalServicesAddForm


class PortalServicesEditForm(form.EditForm):
    """Formulálio de edição de action no portal_actions."""

    label = _(u'Edit link')
    schema = IPortalServicesSettings
    fields = field.Fields(IPortalServicesSettings)

    def getContent(self):

        pip = self.request.get('pid', False)

        if not pip:
            self.request.response.redirect(self.nextURL())

        category = get_category()
        item = category.get(pip, None)

        if not item:
            item = dict(pid='', title='', description='', url_expr='', visible=False)
            self.request.response.redirect(self.nextURL())
        else:
            item = dict(pid=item.id and item.id or '',
                        title=item.title and item.title or '',
                        description=item.description and item.description or '',
                        url_expr=item.url_expr and item.url_expr or '',
                        visible=item.visible)
        return item

    def updateWidgets(self):
        super(PortalServicesEditForm, self).updateWidgets()
        self.widgets['pid'].mode = z3c.form.interfaces.HIDDEN_MODE

    @button.buttonAndHandler(_(u'label_save', default=u'Save'), name='save')
    def handleApply(self, action):
        data, errors = self.extractData()

        if errors:
            self.status = self.formErrorsMessage
            return

        self.applyChanges(data)
        api.portal.show_message(message=_(u'Edit successfully'), request=self.request)
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    @button.buttonAndHandler(_(u'label_cancel', default=u'Cancel'), name='cancel')
    def handleCancel(self, action):
        api.portal.show_message(message=_(u'Edit cancelled'), request=self.request)
        self.request.response.redirect(self.nextURL())

    def applyChanges(self, data):

        pid = data.pop('pid')

        category = get_category()
        item = category.get(pid, None)

        data['url_expr'] = url_expression(data.get('url_expr'))
        for key in data.keys():
            if key in data:
                data[key] = data[key] and data[key] or ''
                item._setPropValue(key, data[key])

    def nextURL(self):
        url = self.context.absolute_url() + '/@@portal-services-settings'
        return url


class PortalServicesEditFormPageWrapper(controlpanel.ControlPanelFormWrapper):
    """Página de configuração do Portal Services"""
    form = PortalServicesEditForm
