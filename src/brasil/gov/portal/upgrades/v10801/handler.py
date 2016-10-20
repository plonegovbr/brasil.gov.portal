# -*- coding: utf-8 -*-
from brasil.gov.agenda.config import PROJECTNAME as AGENDAPROJECTNAME
from brasil.gov.portal.logger import logger
from collective.cover.controlpanel import ICoverSettings
from plone import api
from plone.browserlayer.utils import registered_layers
from plone.browserlayer.utils import unregister_layer
from Products.GenericSetup.tool import UNKNOWN


def atualiza_estilos_cover(portal_setup):
    """Atualiza estilos da configuração do collective.cover caso os mesmos
    tenham sido perdidos. Ver:
    https://github.com/collective/collective.cover/issues/465
    """
    record = '{0}.styles'.format(ICoverSettings.__identifier__)
    old_styles = api.portal.get_registry_record(record)
    new_styles = set([
        'Amarelo|amarelo',
        'Azul Claro - borda|azul-claro-borda',
        'Azul Claro Saude|azul-claro',
        'Azul Escuro Turismo|azul-escuro',
        'Azul Governo|azul',
        'Azul Petroleo Defesa Seguranca|azul-petroleo',
        'Azul Piscina|azul-piscina',
        'Azul Turquesa - borda|azul-turquesa-borda',
        'Azul Turquesa|azul-turquesa',
        'Bege - borda|bege-borda',
        'Bege|bege',
        'Dourado Cultura|dourado',
        'Fio separador|fio-separador',
        'Laranja - borda|laranja-borda',
        'Laranja Cidadania Justica|laranja',
        'Link Externo|link-externo',
        'Lista Horizontal|lista-horizontal',
        'Lista Vertical|lista-vertical',
        'Marrom Claro Economia Emprego|marrom-claro',
        'Marrom Infraestrutura|marrom',
        'Padrao|padrao',
        'Roxo - borda|roxo-borda',
        'Roxo Ciencia Tecnologia|roxo',
        'Verde Claro Meio Ambiente|verde-claro',
        'Verde Escuro Educacao|verde-escuro',
        'Verde Esporte|verde',
    ])
    union_styles = sorted(old_styles.union(new_styles))
    api.portal.set_registry_record(record, set(union_styles))
    logger.info('Estilos do cover atualizados')


def instala_profile_agenda(portal_setup):
    """Instala o profile do brasil.gov.agenda se ele não estiver instalado.
    Em versões antigas do brasil.gov.portal o profile do brasil.gov.agenda não
    era instalado. Ver:
    https://github.com/plonegovbr/brasil.gov.portal/issues/154#issuecomment-78988918
    """
    agenda_profile = '{0}:default'.format(AGENDAPROJECTNAME)
    if portal_setup.getLastVersionForProfile(agenda_profile) == UNKNOWN:
        logger.info('Instalando profile do brasil.gov.agenda')
        profile = 'profile-{0}:default'.format(AGENDAPROJECTNAME)
        portal_setup.runAllImportStepsFromProfile(profile)
        logger.info('Profile do brasil.gov.agenda instalado')


def remove_browserlayer(context):
    """ Remove as browserlayers OEmbedLayer e IPloneAppCollectionLayer
    caso elas ainda estejam registradas"""
    for Ilayer in registered_layers():
        if Ilayer.getName() == 'OEmbedLayer':
            unregister_layer(name=u'collective.oembed')
            logger.info('Layer collective.oembed removida')
        elif Ilayer.getName() == 'IPloneAppCollectionLayer':
            unregister_layer(name=u'plone.app.collection')
            logger.info('Layer plone.app.collection removida')
