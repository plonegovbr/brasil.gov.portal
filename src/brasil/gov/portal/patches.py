# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from collective.z3cform.widgets.multicontent_search_widget import MultiContentSearchFieldWidget
from plone.app.contenttypes.content import Link
from plone.app.contenttypes.migration.dxmigration import DXOldEventMigrator
from plone.app.contenttypes.migration.field_migrators import datetime_fixer
from plone.app.relationfield.behavior import IRelatedItems
from plone.autoform.interfaces import WIDGETS_KEY
from plone.event.utils import default_timezone
from plone.outputfilters.filters import resolveuid_and_caption as base


def outputfilters():
    def patched_call(self, data):
        """ Patch original __call__ """
        data = data.replace('/>', ' />')
        return self.__orig_call__(data)

    setattr(base.ResolveUIDAndCaptionFilter,
            '__orig_call__',
            base.ResolveUIDAndCaptionFilter.__call__)

    setattr(base.ResolveUIDAndCaptionFilter,
            '__call__',
            patched_call)
    logger.info('Patched ResolveUIDAndCaptionFilter')


def link():
    def getRemoteUrl(self):
        return self.remoteUrl

    setattr(Link,
            'getRemoteUrl',
            getRemoteUrl)
    logger.info('Patched Link content type')


def related_items_widget():
    IRelatedItems.setTaggedValue(
        WIDGETS_KEY,
        {'relatedItems': MultiContentSearchFieldWidget}
    )
    logger.info('Patched Related Items widget')


def attendees():
    """

    Da forma como o método migrate_schema_fields está implementado

        https://github.com/plone/plone.app.contenttypes/blob/1.1.1/plone/app/contenttypes/migration/dxmigration.py#L63

    Quando atualizamos o plone.app.contenttypes para 1.1.1 e rodamos os
    upgradeSteps, dá erro em objetos de eventos que não possuem o atributo
    "attendees" (https://github.com/plonegovbr/brasil.gov.portal/blob/master/src/brasil/gov/portal/profiles/initcontent/dados/portal/eventos/evento-1/data.json)
    adicionados automaticamente pelo brasil.gov.portal:

        plone.app.contenttypes-1.1.1-py2.7.egg/plone/app/contenttypes/migration/dxmigration.py", line 74, in migrate_schema_fields
            self.new.attendees = tuple(self.old.attendees.splitlines())
        AttributeError: 'NoneType' object has no attribute 'splitlines'

    Apesar de ter sido sugerido fazer um upgradeStep aqui em brasil.gov.portal
    para setar uma tupla vazia (https://github.com/plonegovbr/brasil.gov.portal/issues/240#issuecomment-305652387)
    isso não funciona pois dá o mesmo erro:

        plone.app.contenttypes-1.1.1-py2.7.egg/plone/app/contenttypes/migration/dxmigration.py", line 74, in migrate_schema_fields
            self.new.attendees = tuple(self.old.attendees.splitlines())
        AttributeError: 'tuple' object has no attribute 'splitlines'

    Esse erro também ocorre se, numa versão plone.app.contenttypes 1.0 você
    adicionar um evento mas não colocar nenhuma informação em attendees.

    Sobra assim a opção do patch logo abaixo.

    FIXME: Se esse erro for corrigido upstream (ver https://github.com/plone/plone.app.contenttypes/issues/414)
    e a versão de plone.app.contenttypes for corrigida no release, esse patch
    pode ser removido.

    """
    def migrate_schema_fields(self):
        timezone = str(self.old.start_date.tzinfo) \
            if self.old.start_date.tzinfo \
            else default_timezone(fallback='UTC')

        self.new.start = datetime_fixer(self.old.start_date, timezone)
        self.new.end = datetime_fixer(self.old.end_date, timezone)

        if hasattr(self.old, 'location'):
            self.new.location = self.old.location
        if hasattr(self.old, 'attendees'):
            # Customização inicia aqui
            # self.new.attendees = tuple(self.old.attendees.splitlines())
            if self.old.attendees:
                self.new.attendees = tuple(self.old.attendees.splitlines())
            else:
                self.new.attendees = tuple()
        # Customização finalizada
        if hasattr(self.old, 'event_url'):
            self.new.event_url = self.old.event_url
        if hasattr(self.old, 'contact_name'):
            self.new.contact_name = self.old.contact_name
        if hasattr(self.old, 'contact_email'):
            self.new.contact_email = self.old.contact_email
        if hasattr(self.old, 'contact_phone'):
            self.new.contact_phone = self.old.contact_phone
        if hasattr(self.old, 'text'):
            # Copy the entire richtext object, not just it's representation
            self.new.text = self.old.text

    setattr(DXOldEventMigrator,
            'migrate_schema_fields',
            migrate_schema_fields)
    logger.info('Patched migrate_schema_fields to help in attendees migration')


def run():
    outputfilters()
    link()
    related_items_widget()
    attendees()
