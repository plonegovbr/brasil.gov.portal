# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone import api


def install_recaptcha(setup_tool):
    """Install recaptcha."""
    addon = 'collective.recaptcha'
    qi = api.portal.get_tool('portal_quickinstaller')
    if qi.isProductInstalled(addon):
        qi.installProducts([addon])
        logger.info(addon + ' was uninstalled')

    portal_types = api.portal.get_tool('portal_types')
    ti = portal_types.getTypeInfo('FormFolder')
    if 'FormCaptchaField' not in ti.allowed_content_types:
        ti.allowed_content_types += ('FormCaptchaField', )
        logger.info('Captcha enabled in PloneFormGen Folder')

    ti = portal_types.getTypeInfo('FieldsetFolder')
    if 'FormCaptchaField' not in ti.allowed_content_types:
        ti.allowed_content_types += ('FormCaptchaField', )
        logger.info('Captcha enabled in PloneFormGen Fieldset')
