# -*- coding: utf-8 -*-
from brasil.gov.portal.logger import logger
from plone.app.contenttypes.content import Link
from plone.app.contenttypes.migration.dxmigration import DXOldEventMigrator
from plone.app.contenttypes.migration.field_migrators import datetime_fixer
from plone.event.utils import default_timezone
from plone.outputfilters.filters import resolveuid_and_caption as base
from Products.contentmigration.basemigrator.migrator import BaseCMFMigrator
from Products.contentmigration.basemigrator.migrator import copyPermMap


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


def attendees_e_timezone():
    """

    attendees
    =========

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
    pode ser removido. Lembrar de alterar no setup.py colocando a versão
    correspondente do plone.app.contenttypes que contenha essa correção.

    timezone
    ========

    Sem esse patch, após rodar os upgradeSteps de plone.app.contenttypes, ao
    tentar acessar a visão de um item do tipo evento, temos o erro:

      Module zope.traversing.adapters, line 136, in traversePathElement
       - __traceback_info__: (None, 'isoformat')
      Module zope.traversing.adapters, line 50, in traverse
       - __traceback_info__: (None, 'isoformat', ())
    LocationError: getField

     - Expression: "data/start/isoformat"
     - Filename:   ... nt-1.1.5-py2.7.egg/plone/app/event/browser/event_view.pt
     - Location:   (line 19: col 60)
     - Source:     ... "dtstart" tal:content="data/start/isoformat">end</li>
                                              ^^^^^^^^^^^^^^^^^^^^
    Isso ocorre porque o método migrate_schema_fields chega a definir um timezone
    mas não atribui ele a self.new.timezone, fazendo uma migração incompleta. Ao
    adicionarmos

        self.new.timezone = timezone

    no método o erro pára de ocorrer.

    FIXME: Se esse erro for corrigido upstream (ver https://github.com/plone/plone.app.contenttypes/issues/424)
    e a versão de plone.app.contenttypes for corrigida no release, esse patch
    pode ser removido. Lembrar de alterar no setup.py colocando a versão
    correspondente do plone.app.contenttypes que contenha essa correção.

    """
    def migrate_schema_fields(self):
        timezone = str(self.old.start_date.tzinfo) \
            if self.old.start_date.tzinfo \
            else default_timezone(fallback='UTC')

        # Customização timezone inicia aqui
        self.new.timezone = timezone
        # Customização timezone finaliza aqui

        self.new.start = datetime_fixer(self.old.start_date, timezone)
        self.new.end = datetime_fixer(self.old.end_date, timezone)

        if hasattr(self.old, 'location'):
            self.new.location = self.old.location
        if hasattr(self.old, 'attendees'):
            # Customização attendess inicia aqui
            # self.new.attendees = tuple(self.old.attendees.splitlines())
            if self.old.attendees:
                self.new.attendees = tuple(self.old.attendees.splitlines())
            else:
                self.new.attendees = tuple()
            # Customização attendess finalizada
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


def reindex_object_after_workflow_migration():
    """
    Após a migração do tipo evento, o título não fica correto e todos os objetos
    do tipo evento ficam como privado, portanto precisamos desse patch que reindexa
    os novos objetos.

    FIXME:
    Se esse erro for corrigido upstream (ver https://github.com/plone/Products.contentmigration/issues/16)
    e a versão de plone.app.contenttypes for corrigida no release, esse patch
    pode ser removido. Lembrar de alterar no setup.py colocando a versão
    correspondente do plone.app.contenttypes que contenha essa correção.
    """
    def migrate_workflow(self):
        """migrate the workflow state
        """
        wfh = getattr(self.old, 'workflow_history', None)
        if wfh:
            wfh = copyPermMap(wfh)
            self.new.workflow_history = wfh
            # INICIO Customização
            self.new.reindexObject()
            # FIM Customização

    setattr(BaseCMFMigrator,
            'migrate_workflow',
            migrate_workflow)
    logger.info('Patched migrate_workflow to help in events migration')


# XXX: workaround for https://github.com/zopefoundation/z3c.form/pull/76
def deselect(self):
    selecteditems = []
    notselecteditems = []
    for selecteditem in self.selectedItems:
        selecteditems.append(selecteditem['value'])
    for item in self.items:
        if not item['value'] in selecteditems:
            notselecteditems.append(item)
    return notselecteditems


def run():
    outputfilters()
    link()
    attendees_e_timezone()
    reindex_object_after_workflow_migration()
