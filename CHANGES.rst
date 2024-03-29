Changelog
---------

2.1.2 (unreleased)
^^^^^^^^^^^^^^^^^^

- Reverte bugfix de campo de ordenação de coleção uma vez que novas versões do Plone possuem o formato esperado por plone.formwidget.querystring.
  `#163 <https://github.com/plonegovbr/brasil.gov.portal/issues/163>`_
  [idgserpro]

- Adiciona plone.app.relationfield de dependência. Esse pacote já era referenciado em alguns xmls dos tipos de contéudo mas não estava explícito no setup.py.
  [idgserpro]

- Adiciona plone.app.stagingbehavior.interfaces.IStagingSupport (recurso de "checkin" e "checkout") para o tipo Capa por padrão.
  `#579 <https://github.com/plonegovbr/brasil.gov.portal/issues/579>`_
  [idgserpro]

- Adiciona patch para Products.CMFPlone.browser.navigation.CatalogNavigationTabs.topLevelTabs
  para substituição do path do site pela url em getRemoteUrl caso use a viewlet
  global sections.
  `#463 <https://github.com/plonegovbr/brasil.gov.portal/issues/463>`__
  [idgserpro]

- Adiciona suporte a plone.app.multilingual em remote_url_utils.
  [idgserpro]

- Adiciona Browser Page remote_url_utils.
  Tratamento do valor de getRemoteUrl ou remoteUrl para evitar que o path do
  site fique exposto nos links.
  `#463 <https://github.com/plonegovbr/brasil.gov.portal/issues/463>`__
  [idgserpro]

- Adiciona patch para Products.CMFPlone.browser.navtree.SitemapNavtreeStrategy.decoratorFactory
  para substituição do path do site pela url em getRemoteUrl.
  `#463 <https://github.com/plonegovbr/brasil.gov.portal/issues/463>`__
  [idgserpro]

- Altera viewlet servicos para que trate o valor de getRemoteUrl através da
  remote_url_utils.
  `#463 <https://github.com/plonegovbr/brasil.gov.portal/issues/463>`__
  [idgserpro]

- Customiza Browser Page link_redirect_view para que trate o valor de remote_url
  através da remote_url_utils; e para que a formação url de links relativos (../, ./)
  deixasse de utilizar como base a url do próprio objeto Link.
  `#463 <https://github.com/plonegovbr/brasil.gov.portal/issues/463>`__
  [idgserpro]

- Adiciona collective.recaptcha. (fecha `#292 <https://github.com/plonegovbr/brasil.gov.portal/issues/292>`_).
  [rodfersou]

- Corrige mecanismo de busca ativa. (fecha `#237 <https://github.com/plonegovbr/brasil.gov.portal/issues/237>`_).
  [rodfersou, agnogueira]

- Adiciona tooltip aos links de redes sociais `#576 <https://github.com/plonegovbr/brasil.gov.portal/issues/576>`_).
  [agnogueira]

- Permite edição do tipo "MPEG Audio File" e "OGG Audio File" através da aba "Conteúdo". (atende parcialmente `#587 <https://github.com/plonegovbr/brasil.gov.portal/issues/587>`_).
  [idgserpro]

- Permite edição do tipo Infográfico através da aba "Conteúdo". (atende parcialmente `#578 <https://github.com/plonegovbr/brasil.gov.portal/issues/578>`_).
  [idgserpro]


2.1.1 (2018-12-08)
^^^^^^^^^^^^^^^^^^

- Adiciona dependência no plone.app.stagingbehavior;
  isso permite habilitar as operações de checkout e checkin para trabalhar em cópias do conteúdo original,
  e evita o erro ``PicklingError: Can't pickle <class 'plone.app.stagingbehavior.interfaces.IStagingSupport'>: import of module plone.app.stagingbehavior.interfaces failed`` ao iniciar as instâncias.
  [hvelarde]

- Adiciona dependência no plone.app.drafts;
  isso evita o erro ``AttributeError: type object 'IDraftStorage' has no attribute 'iro'`` ao iniciar as instâncias.
  [hvelarde]

- Atualizado brasil.gov.temas à versão 2.0.1.
  [hvelarde]


2.1 (2018-12-04)
^^^^^^^^^^^^^^^^

- Atualizado brasil.gov.temas à versão 2.0.
  [hvelarde]

- Nova configuração do webpack não gera arquivo ``_sprite.scss`` (fecha `#563 <https://github.com/plonegovbr/brasil.gov.portal/issues/563>`_).
  [rodfersou]

- Aceita tanto imagens quanto videos como fundo do header expansivel.
  [hvelarde]


2.1rc2 (2018-11-23)
^^^^^^^^^^^^^^^^^^^

- Evita ``KeyError`` ao rodar o upgrade step que conserta a largura das colunas das capas (v10901).
  Caso de erro, uma mensagem no log de eventos indicará o path do objeto com problemas (fecha `#555 <https://github.com/plonegovbr/brasil.gov.portal/issues/555>`_).
  [hvelarde]

- Possibilita tradução de itens na busca da página principal.
  [rodfersou]

- Atualizado brasil.gov.temas à versão 2.0rc1.
  [hvelarde]

- Atualizado brasil.gov.tiles à versão 2.0rc1.
  [hvelarde]

- Atualizado brasil.gov.agenda à versão 2.0b1.
  [hvelarde]

- Adiciona informação de direitos autorais à imagem principal das notícias.
  [rodfersou]

- Atualizado brasil.gov.barra à versão 3.0.6.
  [hvelarde]

- Corrige o valor da propriedade ``default_view`` no factory do tipo de conteúdo Artigo para portais migrados (fecha `#552 <https://github.com/plonegovbr/brasil.gov.portal/issues/552>`_).
  [hvelarde]


2.1rc1 (2018-10-17)
^^^^^^^^^^^^^^^^^^^^

- Atualizado brasil.gov.temas à versão 2.0b5.
  [hvelarde]

- Corrige viewlet que mostra link para voltar para o topo.
  [rodfersou]

- Move scripts do contraste para o pacote brasil.gov.temas.
  [rodfersou]

- Atualiza configuração do webpack.
  [rodfersou]

- Corrige entradas do portal actions.
  [rodfersou]

- Corrige tradução de viewlet de redes.
  [rodfersou]

- Atualizado collective.fingerpointing à versão 1.8.
  [hvelarde]

- Atualizado collective.lazysizes à versão 4.1.4.
  [hvelarde]

- Adiciona viewlet para mostrar texto da licença de uso.
  [rodfersou]


2.1.1b1 (2018-10-05)
^^^^^^^^^^^^^^^^^^^^

- Atualizado brasil.gov.temas à versão 2.0b4.
  [hvelarde]

- Atualizado brasil.gov.barra à versão 3.0.5.
  [hvelarde]

- Corrige estilos para tiles do collective.cover.
  [hvelarde]

- Atualizado collective.cover à versão 1.8b2.
  [hvelarde]

- Adiciona novamente dependência no plone4.csrffixes.
  [hvelarde]

- Atualizado collective.lazysizes à versão 4.1.2.
  [hvelarde]


2.1b1 (2018-09-28)
^^^^^^^^^^^^^^^^^^

- Atualizado brasil.gov.agenda à versão 2.0a7.
  [hvelarde]

- Atualizado brasil.gov.temas à versão 2.0b3.
  [hvelarde]

- Atualizado brasil.gov.tiles à versão 2.0b3.
  [hvelarde]

- Atualizado collective.cover à versão 1.8b1.
  [hvelarde]

- Adiciona funcionalidade de preview de imagens em links.
  [rodfersou]

- Adiciona suporte para processamento de recursos estáticos usando o `webpack <https://webpack.js.org/>`_.
  [rodfersou]

- Corrige upgrade step para desinstalar o ``Products.Doormat`` (fecha `#523 <https://github.com/plonegovbr/brasil.gov.portal/issues/523>`_).
  [hvelarde]

- Corrige estilos para tiles do collective.cover.
  [hvelarde]

- Atualizado brasil.gov.barra à versão 2.0b1.
  [hvelarde]


2.0b3 (2018-09-19)
^^^^^^^^^^^^^^^^^^

- Atualizado brasil.gov.tiles à versão 2.0b2.
  [hvelarde]

- Atualizado collective.cover à versão 1.7b5.
  [hvelarde]

- Atualizado plone.restapi à versão 3.4.5.
  [hvelarde]

- Corrige opções iniciais do menu de navegação.
  [hvelarde]

- Instala webcouturier.dropdownmenu ao atualizar o site.
  [hvelarde]

- Evita instalar plone.restapi em novos portais (refs. `plone.rest#73 <https://github.com/plone/plone.rest/issues/73>`_).
  [hvelarde]

- Atualizado Plone à versão 4.3.18.
  [hvelarde]

- Atualizado collective.lazysizes à versão 4.1.1.1.
  [hvelarde]


2.0b2 (2018-09-04)
^^^^^^^^^^^^^^^^^^

- Atualizado brasil.gov.temas à versão 2.0b2.
  [hvelarde]

- Atualizado brasil.gov.tiles à versão 2.0b1.
  [hvelarde]

- Atualiza i18n e traduções ao Português Brasileiro.
  [agnogueira, hvelarde]

- Remove validador do tamanho da imagem de fundo do cabeçalho (fecha `#520 <https://github.com/plonegovbr/brasil.gov.portal/issues/520>`_).
  [hvelarde]

- Adiciona novos estilos para o cover.
  [agnogueira]


2.0b1 (2018-09-03)
^^^^^^^^^^^^^^^^^^
- Adiciona tamanhos de miniaturas de imagens de acordo com a largura de colunas do portal.
  [agnogueira]

- Atualizado brasil.gov.tiles à versão 2.0a1.
  [hvelarde]

- Remove da configuração referências a tiles descontinuados.
  [hvelarde]

- Atualizado brasil.gov.agenda à versão 2.0a6.
  [hvelarde]

- Atualizado brasil.gov.portlets à versão 2.0a1.
  [hvelarde]

- Atualizado brasil.gov.temas à versão 2.0b1.
  [hvelarde]

- Corrige ``UnicodeDecodeError`` no header do portal (fecha `#515 <https://github.com/plonegovbr/brasil.gov.portal/issues/515>`_).
  [claytonc]

- Desinstala ``Products.Doormat`` pois ele não é mais usado no projeto;
  remove também todas as customizações do complemento.
  [hvelarde]

- Adiciona visäo de Filtro de resultados.
  [rodfersou, hvelarde]

- Adiciona visão de Central de conteúdo.
  [rodfersou, hvelarde]

- Atualiza as dependências do pacote.
  Remove dependência no ``plone.directives.form`` e últimos traços do Grok.
  [hvelarde]

- Adiciona opção para permitir escolher entre headers diferentes.
  [hvelarde, rodfersou]

- Adiciona https nas URLs das redes sociais.
  [agnogueira]

- Corrige workflow para tipo de conteúdo Infográfico.
  [rodfersou]

- Altera configurações do cover (grid, estilos e modelos).
  [agnogueira]

- Remove viewlet de destaques e dependência direta no five.grok.
  [hvelarde]

- Corrige dependências do pacote.
  [hvelarde]

- Remove customização desnecessária do portlet de navegação.
  [hvelarde]

- Corrige a largura das columnas das capas de acordo ao novo layout.
  [hvelarde]

- Remove todos os portlets atribuídos à raíz do site.
  [hvelarde]

- Corrige ``AttributeError`` e outros problemas no upgrade step v10900 (fecha `#448 <https://github.com/plonegovbr/brasil.gov.portal/issues/448>`_).
  [hvelarde]

- Atualizado Products.PloneKeywordManager à versão 2.2.1.
  [hvelarde]

- Remove IDs das redes sociais para evitar duplicidade.
  [agnogueira]

- Atualizado collective.cover à versão 1.7b3.
  [hvelarde]


2.0a5 (2018-07-06)
^^^^^^^^^^^^^^^^^^

.. Warning::
    Atualizações da branch 1.x do pacote só serão suportadas da versão mais recente dessa branch.
    O collective.portlet.calendar não é mais uma dependência do brasil.gov.agenda;
    é necessário adicioná-lo como dependência no buildout para permitir sua remoção.
    Consulte a documentação do release para obter mais informação.

- Atualizado collective.cover à versão 1.7b2.
  [hvelarde]

- Atualizado brasil.gov.temas à versão 2.0a6.
  [hvelarde]

- Atualizado brasil.gov.agenda à versão 2.0a4.
  [hvelarde]

- Remove collective.portlet.calendar da lista de pacotes ocultos;
  esse pacote não é mais dependência do brasil.gov.agenda.
  [hvelarde]

- Atualizado plone.restapi à versão 3.1.0.
  [hvelarde]

- Atualizado Products.PloneFormGen à versão 1.7.24.
  [hvelarde]

- Atualiza versão do profile usado para 10900 (closes `#472 <https://github.com/plonegovbr/brasil.gov.portal/issues/472>`_).
  [hvelarde]

- Atualizado Plone à versão 4.3.17.
  [hvelarde]


2.0a4 (2018-06-06)
^^^^^^^^^^^^^^^^^^

- Adiciona dependência no `six <https://pypi.org/project/six/>`_ para futura compatibilidade com Python 3.
  [hvelarde]

- Adiciona suporte para gestão de tags.
  [hvelarde]

- Remove dependência no plone4.csrffixes.
  [hvelarde]

- Adiciona um viewlet para relatórios de erros;
  é preciso criar um formulário de contato com id ``relatar-erros`` na raiz do site para utilizar este recurso.
  [hvelarde, claytonc]

- Atualiza as traduções a português brasileiro e espanhol.
  [hvelarde]

- Revisa a view de galeria de fotos e atualiza a lista de dimensões de imagens validas.
  [rodfersou]

- Corrige o viewlet services responsável pelos links de destaques.
  [claytonc]

- Adiciona um configlet para gerenciar os links no portal tabs.
  [claytonc]

- Adicionado tipo de conteúdo ``Infografic``;
  por enquanto é simplesmente um clone do tipo de conteúdo ``Image``.
  [hvelarde]


2.0a3 (2018-02-28)
^^^^^^^^^^^^^^^^^^

- Atualiza código para usar os decoradores ``implementer`` e ``adapter`` da ZCA.
  [hvelarde]

- Corrige ``icon_expr`` dos tipos de conteúdo definidos no pacote.
  [hvelarde]

- Corrige as permissões ``brasil.gov.portal: Add MPEG File`` e ``brasil.gov.portal: Add OGG File``:
  um usuário com papel "Editor" não deve poder adicionar conteúdo.
  [hvelarde]

- Atualizado plone.restapi à versão 1.1.0.
  [hvelarde]

- Atualizado brasil.gov.barra à versão 1.2.3.
  [hvelarde]

- Atualizado brasil.gov.temas à versão 2.0a4.
  [hvelarde]

- Corrige alinhamento do topo quando não informada primeira linha do título.
  [rodfersou]

- Habilita a busca de objetos de tipo ``sc.embedder``.
  [hvelarde]

2.0a2 (2018-01-11)
^^^^^^^^^^^^^^^^^^

- Atualizado sc.social.like à versão 2.13b3.
  [hvelarde]

- Remove monkey patches relacionados à atualização do plone.app.contenttypes.
  [hvelarde]

- Corrige configuração padrão do sc.social.like.
  [hvelarde]

- Adiciona patch para o widget de campos ordenados não engolir opções com mesmo nome (refs. `z3c.form#76 <https://github.com/zopefoundation/z3c.form/pull/76>`_).
  [rodfersou]

- Evita ``KeyError`` nos resultados da busca provocado por verbetes inexistentes.
  [hvelarde]


2.0a1 (2017-12-27)
^^^^^^^^^^^^^^^^^^

- Atualizado brasil.gov.vcge à versão 2.0.2 (ainda não é possível a migração de 1.x).
  [hvelarde]

- Adiciona webcouturier.dropdownmenu ao IDG;
  habilita menus dropdown para navegação global.
  [hvelarde]

- Implementa importação de conteúdo usando formato JSON e collective.transmogrifier.
  [hvelarde]

- Remove customizações dos templates do collective.nitf.
  [hvelarde]

- O viewlet ``global_sections`` é visível novamente.
  [rodfersou]

- Move estilos para o pacote brasil.gov.temas.
  [rodfersou]

- Remove criação de estrutura e conteúdo iniciais.
  [hvelarde]

- Remove dependência no collective.z3cform.widgets.
  [hvelarde]

- Removidos upgrade steps anteriores a v10803.
  [hvelarde]
