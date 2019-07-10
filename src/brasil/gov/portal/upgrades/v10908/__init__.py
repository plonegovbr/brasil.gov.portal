# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


def enable_livesearch(setup_tool):
    """Enable livesearch by default."""
    settings = api.portal.get_tool('portal_properties').site_properties
    if not settings.enable_livesearch:
        settings.enable_livesearch = True
        logger.info('Live search enabled.')


def install_recaptcha(setup_tool):
    """Install recaptcha."""
    addon = 'collective.recaptcha'
    qi = api.portal.get_tool('portal_quickinstaller')
    if not qi.isProductInstalled(addon):
        qi.installProducts([addon])
        logger.info(addon + ' was installed')

    portal_types = api.portal.get_tool('portal_types')
    ti = portal_types.getTypeInfo('FormFolder')
    if 'FormCaptchaField' not in ti.allowed_content_types:
        ti.allowed_content_types += ('FormCaptchaField', )
        logger.info('Captcha enabled in PloneFormGen Folder')

    ti = portal_types.getTypeInfo('FieldsetFolder')
    if 'FormCaptchaField' not in ti.allowed_content_types:
        ti.allowed_content_types += ('FormCaptchaField', )
        logger.info('Captcha enabled in PloneFormGen Fieldset')
