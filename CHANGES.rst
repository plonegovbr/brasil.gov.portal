Changelog
---------

2.0a4 (unreleased)
^^^^^^^^^^^^^^^^^^

- Adiciona um configlet para gerenciar os links no portal tabs.
  [claytonc.sousa]

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
