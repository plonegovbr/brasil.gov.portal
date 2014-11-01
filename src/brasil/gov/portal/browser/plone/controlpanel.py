# -*- coding: utf-8 -*-
from plone.app.controlpanel.overview import OverviewControlPanel as ControlPanelView

import pkg_resources


class OverviewControlPanel(ControlPanelView):
    def portal_padrao_version(self):
        """Retorna versão do Portal Padrão
        """
        get_dist = pkg_resources.get_distribution
        return get_dist('brasil.gov.portal').version

    def version_overview(self):
        """Lista versões de produtos instalados
        """
        versions = super(OverviewControlPanel, self).version_overview()
        versions.insert(
            0,
            u'Portal Padrão {0}'.format(self.portal_padrao_version())
        )
        return versions
