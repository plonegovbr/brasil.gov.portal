# -*- coding: utf-8 -*-
from collective.nitf.browser import View as CollectiveNITFView
from plone.app.layout.viewlets.content import ContentRelatedItems


class View(CollectiveNITFView):
    """Customize NITF view
    """

    def get_related_items(self):
        """
        Como ainda customizamos a visão de nitf, na versão 1.x de
        collective.nitf, tínhamos o atributo relatedItems no tipo nitf. Na
        template customizada, renderizávamos o widget presente em
        collective.z3cform.widgets, pro campo relatedItems (esses são os objetos
        que eram disponibilizados em nitf_custom_view na div newsRelatedItems).

        <NITF at conheca-o-novo-modelo-da-identidade-digital-padrao-do-governo-federal>
        [<z3c.relationfield.relation.RelationValue object at 0x7f15d8575cf8>]
        <brasil.gov.portal.browser.content.nitf_custom_view.View object at 0x7f15d6c72f90>
        {'byline': <TextWidget 'form.widgets.byline'>,
        'subtitle': <TextWidget 'form.widgets.subtitle'>,
        'text': <RichTextWidget 'form.widgets.text'>,
        'section': <SelectWidget 'form.widgets.section'>,
        'relatedItems': <MultiContentSearchWidget 'form.widgets.relatedItems'>,
        'location': <TextWidget 'form.widgets.location'>,
        'genre': <SelectWidget 'form.widgets.genre'>,
        'urgency': <SelectWidget 'form.widgets.urgency'>}

        Acontece que após os commits:

        https://github.com/collective/collective.nitf/commit/a4704e26210cbdf5aadd473503d14947034a613a

        https://github.com/collective/collective.nitf/commit/5a27baa54f728f1de123c6883e02020b481d7d00

        Esse campo foi completamente removido e portanto ao atualizar para 2.x
        dá erro na renderização da template que ainda espera esses atributos.

        Dessa forma, usaremos o método padrão da viewlet do Plone de retornar
        itens relacionados, e montaremos na template com o mesmo html que o
        widgets da versão 1.x montaria mantendo assim o layotu padrão.
        """
        viewlet = ContentRelatedItems(self.context, self.request, None, None)
        return viewlet.related_items()

    def show_more_images(self):
        return len(self.get_images()) > 1

    def get_link_erros(self):
        portal_obj = self.context.portal_url.getPortalObject()
        if (hasattr(portal_obj, 'relatar-erros')):
            return self.context.absolute_url() + '/relatar-erros'
        elif (hasattr(portal_obj, 'report-erros')):
            return self.context.absolute_url() + '/report-erros'
        elif (hasattr(portal_obj, 'informe-de-errores')):
            return self.context.absolute_url() + '/informe-de-errores'
        else:
            return None
