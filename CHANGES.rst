Changelog
---------

2.0a2 (unreleased)
^^^^^^^^^^^^^^^^^^

- Remove monkey patches relacionados à atualização do plone.app.contenttypes.
  [hvelarde]

- Corrige configuração padrão do sc.social.like.
  [hvelarde]

- Adiciona parche para o widget de campos ordenados não engolir opções com mesmo nome (refs. `z3c.form#76 <https://github.com/zopefoundation/z3c.form/pull/76>`_).
- Move scripts do contraste para o pacote brasil.gov.temas.
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
