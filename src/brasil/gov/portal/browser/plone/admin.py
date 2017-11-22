# -*- coding: utf-8 -*-
"""Overrides Products/CMFPlone/browser/admin.py

XXX: we need to think how to reduce the pain of keeping this in sync.

isort:skip_file
"""
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides

from AccessControl import getSecurityManager
from AccessControl.Permissions import view as View

from Products.CMFCore.permissions import ManagePortal
from Products.CMFPlone.factory import _DEFAULT_PROFILE
from Products.CMFPlone.factory import addPloneSite
from Products.CMFPlone.interfaces import IPloneSiteRoot

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.admin import AddPloneSite as AddPloneSiteView
from Products.CMFPlone.browser.admin import Overview as OverviewView


class Overview(OverviewView):

    def sites(self, root=None):
        if root is None:
            root = self.context

        result = []
        secman = getSecurityManager()
        for obj in root.values():
            if IPloneSiteRoot.providedBy(obj):
                if secman.checkPermission(View, obj):
                    result.append(obj)
            elif obj.getId() in getattr(root, '_mount_points', {}):
                result.extend(self.sites(root=obj))
        return result

    def outdated(self, obj):
        mig = obj.get('portal_migration', None)
        if mig is not None:
            return mig.needUpgrading()
        return False

    def can_manage(self):
        secman = getSecurityManager()
        return secman.checkPermission(ManagePortal, self.context)

    def upgrade_url(self, site, can_manage=None):
        if can_manage is None:
            can_manage = self.can_manage()
        if can_manage:
            return site.absolute_url() + '/@@plone-upgrade'
        else:
            return self.context.absolute_url() + '/@@plone-root-login'


class AddPloneSite(AddPloneSiteView):

    def __call__(self):
        context = self.context
        form = self.request.form
        extension_ids = form.get('extension_ids', [])
        extension_ids.insert(0, 'brasil.gov.portal:default')
        # Criamos com conteúdo inicial
        extension_ids.insert(1, 'brasil.gov.portal:initcontent')
        # Dados do formulario
        orgao = form.get('orgao', '')
        url_orgao = form.get('url_orgao', '')
        title_1 = form.get('title_1', '')
        title_2 = form.get('title_2', '')
        title = '%s %s' % (title_1, title_2)
        # Se o formulario tiver sido enviado, criaremos o site
        submitted = form.get('form.submitted', False)
        if submitted:
            alsoProvides(self.request, IDisableCSRFProtection)
            site_id = form.get('site_id', 'portal')
            # Criacao do site
            site = addPloneSite(
                context, site_id,
                title=title,
                description=form.get('description', ''),
                profile_id=form.get('profile_id', _DEFAULT_PROFILE),
                extension_ids=extension_ids,
                setup_content=False,
                default_language='pt-br',
            )
            # Atualizacao de propriedades do site
            site.manage_changeProperties(
                title=title,
                title_1=title_1,
                title_2=title_2,
                orgao=orgao,
            )
            pprop = getToolByName(self.context, 'portal_properties')
            configs = getattr(pprop, 'brasil_gov', None)
            configs.manage_changeProperties(url_orgao=url_orgao)
            self.request.response.redirect(site.absolute_url())

        return self.index()
