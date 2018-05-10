# -*- coding: utf-8 -*-
from Products.Doormat.browser.views import DoormatView as BaseView


# FIXME
# BBB
# Essa customização, a partir do Products.Doormat 1.2, poderá ser
# completamente removida. Para maiores detalhes, veja
# https://github.com/plonegovbr/brasil.gov.portal/issues/95#issuecomment-229473089
# Ver se não existe algum teste associado a essa customização para que também
# seja removido.
class DoormatView(BaseView):
    """ Doormat View lidando com os dados de links
    """

    def getDoormatData(self):
        """ Return a dictionary like this:
        data = [
            {   'column_title: 'Column One',
                'column_sections: [
                {   'section_title': 'De Oosterpoort',
                    'section_links': [
                        {   'link_title': 'Some Title',
                            'link_url': 'http://some.whe.re',
                            'link_class': 'external-link',
                            'content': 'html content',
                            },
                        ]
                    },
                ]
            },
        ]
        """
        portal_state = self.context.restrictedTraverse('@@plone_portal_state')
        navigation_root_url = portal_state.navigation_root_url()
        portal_url = portal_state.portal_url()
        data = super(DoormatView, self).getDoormatData()
        for column in data:
            for section in column['column_sections']:
                for link in section['section_links']:
                    link_url = link['link_url']
                    url = link_url
                    if '${navigation_root_url}' in link_url:
                        url = link_url.replace(
                            '${navigation_root_url}',
                            navigation_root_url)
                    elif '${portal_url}' in link_url:
                        url = link_url.replace(
                            '${portal_url}',
                            portal_url)
                    link['link_url'] = url
        return data
