# -*- coding: utf-8 -*-
from brasil.gov.portal.config import SHOW_DEPS
from brasil.gov.portal.logger import logger
from brasil.gov.portal.setuphandlers import _instala_pacote
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile


def apply_profile(context):
    """Atualiza perfil para versao 10300"""
    profile = 'profile-brasil.gov.portal.upgrades.v10300:default'
    loadMigrationProfile(context, profile)
    logger.info('Atualizado para versao 10300')


def atualiza_secoes(context):
    """Remove referencias a secao General. Alteramos para Noticias"""
    ct = api.portal.get_tool('portal_catalog')
    resultados = ct.searchResults(
        section='General',
        portal_type='collective.nitf.content',
    )
    logger.info(u'{0} conteúdos na seção General'.format(len(resultados)))
    for item in resultados:
        # Alteramos para Noticias
        o = item.getObject()
        o.section = u'Notícias'
        o.reindexObject(idxs=['section'])
    logger.info('Conteudos atualizados')

    available_sections = list(api.portal.get_registry_record(
        'collective.nitf.controlpanel.INITFSettings.available_sections'))
    if 'General' in available_sections:
        available_sections.remove('General')
        logger.info('Remove secao General')
    if u'Notícias' not in available_sections:
        available_sections.append(u'Notícias')
        logger.info('Adiciona secao Noticias')
    # Adiciona a secao Noticias
    api.portal.set_registry_record(
        'collective.nitf.controlpanel.INITFSettings.available_sections',
        set(available_sections))
    default_section = api.portal.get_registry_record(
        'collective.nitf.controlpanel.INITFSettings.default_section')
    if default_section == 'General':
        api.portal.set_registry_record(
            'collective.nitf.controlpanel.INITFSettings.default_section',
            u'Notícias')
        logger.info('Define Noticias como secao padrao')


def atualiza_pacotes_instalados(context):
    """Exibe pacotes de dependencias"""
    logger.info(u'Rotina para exibir pacotes de dependências')
    qi = api.portal.get_tool('portal_quickinstaller')

    for p in SHOW_DEPS:
        _instala_pacote(qi, p)
        logger.info(u'Exibe pacote {0}'.format(p))
