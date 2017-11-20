Changelog
---------

1.6rc1 (unreleased)
^^^^^^^^^^^^^^^^^^^

- Adiciona hotfix de segurança `20171128 <https://plone.org/security/hotfix/20171128>`_.
  [hvelarde]

- Atualizado collective.cover à versão 1.6b5;
  corrige o crecimento exponencial dos objetos quando se usa versionamento.
  [hvelarde]

- Corrige proteção CSRF na adição de sites;
  atualiza views e templates de Plone para facilitar manutenção.
  [hvelarde]


1.5 (2017-11-20)
^^^^^^^^^^^^^^^^

- Atualizado brasil.gov.barra à versão 1.2.2.
  [hvelarde]


1.5rc2 (2017-11-13)
^^^^^^^^^^^^^^^^^^^

.. Warning::
    O collective.z3cform.widgets ainda é uma dependência do IDG,
    mas após esta atualização ele não será mais utilizado nem será possível instalá-lo.
    A dependência será removida completamente em a versão 2.0.

- Atualizado brasil.gov.tiles à versão 1.5.1.
  [hvelarde]

- Atualizado brasil.gov.temas à versão 1.2.4.
  [hvelarde]

- Atualizado brasil.gov.agenda à versão 1.1.2.
  [hvelarde]

- Adiciona suporte a âncoras de links internos: antes não era possível adicionar um link do tipo interno numa página que referenciava uma âncora adicionada em outro documento. Alterando as regras do TinyMCE isso agora é possível. Para entender melhor essa funcionalidade, basta rodar o test_tinymce_ancora.robot localmente.
  [idgserpro]

- Habilita os ícones dos conteúdos para os usuários autenticados (fecha `#343 <https://github.com/plonegovbr/brasil.gov.portal/issues/343>`_).
  [claytonc]

- Revisa estilos "Normal", "Grande" e "Gigante" para a nova versão do collective.cover (fecha `#356 <https://github.com/plonegovbr/brasil.gov.portal/issues/356>`_).
  [rodfersou]

- Habilita suporte para `RESTful Hypermedia API <https://pypi.python.org/pypi/plone.restapi>`_ no IDG.
  [hvelarde]

- Desinstala collective.z3cform.widgets e o browser layer associado.
  [hvelarde]

- Adiciona collective.fingerpointing ao IDG;
  se instalado, habilita um log de auditoria simples no portal.
  [hvelarde]

- Adiciona collective.liveblog ao IDG;
  se instalado, habilita o tipo de conteúdo Liveblog (uma ferramenta para cobertura ampla de um evento em curso) no portal.
  [hvelarde]

- Adiciona sc.photogallery ao IDG;
  se instalado, habilita o tipo de conteúdo Galeria de fotos, com uma visão slideshow e possibilidade de download, no portal.
  [hvelarde]

- Adiciona collective.lazysizes ao IDG;
  se instalado, habilita lazy loading de imagens e iframes no conteúdo do portal.
  [hvelarde]

- Adiciona Products.RedirectionTool ao IDG;
  habilita gerenciamento dos alias da redirection tool (plone.app.redirector).
  [hvelarde]

- Atualizado plone.app.contenttypes à versão 1.1.5.
  [hvelarde]

- Atualizado Products.PloneFormGen à versão 1.7.23.
  [hvelarde]

- Atualizado sc.social.like à versão 2.13b2;
  consulte a documentação do release para mais informação sobre as novas funcionalidades.
  [hvelarde]


1.4 (2017-11-07)
^^^^^^^^^^^^^^^^

- Corrige carga da seção "Em destaque" (fecha `#401 <https://github.com/plonegovbr/brasil.gov.portal/issues/401>`_).
  [hvelarde]

- Corrige visão sumária para o tipo de conteúdo Evento (fecha `#397 <https://github.com/plonegovbr/brasil.gov.portal/issues/397>`_).
  [hvelarde]

- Corrige configuração padrão do collective.upload (fecha `#392 <https://github.com/plonegovbr/brasil.gov.portal/issues/392>`_).
  [hvelarde]


1.4rc1 (2017-11-01)
^^^^^^^^^^^^^^^^^^^

.. Warning::
    Após atualização das versões do setuptools e do zc.buildout será necessário dar bootstrap no projeto novamente antes de rodar o buildout.
    Consulte a documentação do release para mais informação.

- Atualizado Plone à versão 4.3.15.
  [hvelarde]

- Atualizado zc.buildout à versão 2.9.5;
  isso corrige um problema na descarga de eggs do PyPI usando HTTPS e melhora a performance do Buildout.
  [hvelarde]

- Remove dependência no five.grok (exeto do brasil.gov.paginadestaque e do viewlet de destaques) (fecha `#373 <https://github.com/plonegovbr/brasil.gov.portal/issues/375>`_).
  [hvelarde]

- Atualizado brasil.gov.vcge à versão 1.1.1.
  [hvelarde]

- Atualizado brasil.gov.tiles à versão 1.5.
  [hvelarde]

- Atualizado brasil.gov.temas à versão 1.2.3;
  isso corrige um erro na aparência do portal após o login (fecha `#318 <https://github.com/plonegovbr/brasil.gov.portal/issues/318>`_).
  [hvelarde]

- Atualizado brasil.gov.barra à versão 1.2.1.
  [hvelarde]

- Atualizado collective.cover à versão 1.6b4.
  [hvelarde]

- Atualizado collective.polls à versão 1.10b1.
  [hvelarde]

- Atualizado collective.upload à versão 9.18.0rc2.
  Remove customização dos templates do collective.upload.
  [hvelarde]

- Remove customização desnecessária do viewlet de itens relacionados (fecha `#355 <https://github.com/plonegovbr/brasil.gov.portal/issues/355>`_).
  [hvelarde]

- Atualizado sc.embedder à versão 1.5b1;
  isso adiciona pesquisa por tags ao tipo de conteúdo Embedder.
  Remove customização do template do sc.embedder.
  [hvelarde]

- Atualizado collective.nitf à versão 2.1b4;
  isso adiciona pesquisa por tags ao tipo de conteúdo Artigo (corrige `#155 <https://github.com/plonegovbr/brasil.gov.portal/issues/155>`_).
  [hvelarde]


1.3 (2017-10-05)
^^^^^^^^^^^^^^^^

- Substitue o h1 por div no portal logo para adequar o portal a acessibilidade.
  Se você possui temas customizados baseados no desse pacote, lembre-se de revisá-los para corrigir possíveis incompatibilidades.
  [idgserpro]

- Altera a viewlet de site actions para retirar o atributo title dos links para adequar as regras de acessibilidade.
  [idgserpro]

- Altera a viewlet de serviços para incluir a descrição do objeto no atributo title do link para adequar as regras de acessibilidade.
  [idgserpro]

- Insere descrição para os links vazios acontent, anavigation e afooter para atender aos critérios de acessibilidade.
  [idgserpro]

- Altera a viewlet de serviços para obter a url do link do atributo remoteUrl do tipo Link.
  [idgserpro]

- Altera o valor do atributo remoteUrl dos links da pasta /rodape/coluna-2 para que fiquem iguais aos links da viewlet de serviços evitando assim erros de acessibilidade.
  [idgserpro]

- Corrige erro de regressão na exibição da data na visão sumária. Com a atualização do plone.app.contenttypes, a lógica da template precisa chamar um método e não um atributo indexado de um brain. (relacionado a `#157`_).
  [idgserpro]


1.2 (2017-09-22)
^^^^^^^^^^^^^^^^

- Atualiza as dependências do pacote.
  [hvelarde]


1.2rc1 (2017-09-21)
^^^^^^^^^^^^^^^^^^^

.. Warning::
   ATENÇÃO:
   1 - Com a atualização de plone.app.contenttypes para 1.1.1 nesse release
   plone.app.event foi atualizado e, com ele, a necessidade de adição de uma
   variável TZ (timezone) no seu buildout na seção environment-vars ANTES de
   atualizar para essa versão. Se você não usa o buildout de exemplo portal.buildout,
   segue um exemplo de como adicionar em seu buildout:
   https://github.com/plonegovbr/portal.buildout/blob/d9e084275977b45ad5349057f95b05dda70db49a/buildout.d/base.cfg#L39
   2 - Caso não esteja na última versão do marco 1.1.x (hoje a 1.1.5.3) recomendamos
   que se atualize para essa versão antes de atualizar direto para 1.2.x. Lembre-se
   de que o release IDG, com todas as suas dependências, pode ter um número diferente
   do brasil.gov.portal. Para mais informações, leia
   https://github.com/plonegovbr/portalpadrao.release/blob/1710d6261e53a629093933119d9c76d0708ae534/README.md#user-content-como-escolher-corretamente-o-arquivo-de-versões-de-um-release
   3 - No momento de executar os upgradeSteps para esse release, os de
   brasil.gov.portal devem ser os últimos a serem executados. Para entender
   melhor o uso de upgradeSteps leia
   http://identidade-digital-de-governo-plone.readthedocs.io/en/latest/atualizacao/

- Corrige templates para que os testes test_collection_summary_view
  e test_collection_listing_view que estavam como @unittest.expectedFailure
  possam funcionar novamente. (closes `#359`_).
  [idgserpro]

- Faz um patch nos upgrades de plone.app.contenttypes 1.0 para 1.1.1 e
  Products.contentmigration para resolver problemas com o tipo evento e com a
  reindexação dos itens migrados. (relacionado a `#360`_).
  [idgserpro]

- Corrige objetos eventos do conteúdo inicial (closes `#360`_).
  [idgserpro]


1.2b1 (2017-07-07)
^^^^^^^^^^^^^^^^^^

.. Warning::
   ATENÇÃO: No momento de executar os upgradeSteps para esse release, os de
   brasil.gov.portal devem ser os últimos a serem executados.

- Atualiza plone.app.contenttypes para a versão do Plone (1.1.1) (closes `#240`_).
  [idgserpro]

- Prepara pacote para ser compatível com novas versões de collective.nitf a
  partir da versão 2.1b2. (closes `#349`_).
  [idgserpro]


1.1.5.1 (2016-11-07)
^^^^^^^^^^^^^^^^^^^^

- Conserta ``_corrige_css_class``, upgradeStep 10700.
  [idgserpro]


1.1.5 (2016-11-07)
^^^^^^^^^^^^^^^^^^

* Corrige pickling errors entre upgradesteps ao retirar a layer do
  collective.oembed e plone.app.collection.
  [idgserpro]

* Na viewlet NITFBylineViewlet, deixamos de buscar dados do usuário quando o
  autor é indefinido (closes `#320`_).
  [tcurvelo]

* Corrige a exibição de notícias com portlets, além de outras páginas onde seja
  usado o CSS selector div.width-1:2. (closes `#303`_).
  [finnicius]

* Adiciona diretiva do plone4.csrffixes no dependencies.zcml (closes `#279`_).

* Corrige upgradeStep 10700 para que execute o método "simplify_layout" do
  collective.cover, necessário para se evitar quebra de capa dependendo da
  ordem em que os upgradeSteps são executados. (closes `#289`_)
  [idgserpro]

* Corrige o "Link to Collection" impedindo que o rodapé desse erro com links
  para coleções. (closes `#95`_).
  [idgserpro]

* Complementa a css das tiles (closes `#189`_).
  [idgserpro]

* Upgrade step que instala profile do brasil.gov.agenda se não estiver
  instalado e atualiza os estilos do collective.cover(closes `#154`_).
  [idgserpro]


1.1.4 (2016-03-14)
^^^^^^^^^^^^^^^^^^

* Corrige erro de exibição da data na visão sumária (closes `#157`_).
  [winstonf88]

* Corrige erro na criação de capas (closes `#242`_).
  [winstonf88]

* Corrige falha no carregamento dos destaques com visão padrão (closes `#167`_).
  [winstonf88]

* Corrige conteúdo inicial de tiles que possuem um uuid de referência a um
  objeto que não existe. (closes `#275`_).
  [idgserpro]

* Corrige erro de layout na visão de galeria (closes `#205`_).
  [winstonf88]

* Corrige erro de exibiçao dos botões de redes sociais (closes `#156`_).
  [winstonf88]

* Adiciona opção para esconder a data de publicação ou o autor de um conteúdo (closes `#202`_).
  [idgserpro]

* Corrige falha nos testes (closes `#241`_).
  [winstonf88]

* Corrige ícones de redes sociais cortados (closes `#203`_).
  [winstonf88]


1.1.3 (2015-09-30)
^^^^^^^^^^^^^^^^^^

* Reindexa capas para corrigir erro de consulta no catalog (closes `#226`_).
  [winstonf88]

* Adiciona `Products.PloneHotfix20150910 <https://pypi.python.org/pypi/Products.PloneHotfix20150910>`_ como dependência do pacote (closes `#232`_).
  [idgserpro]

* Corrige a execução do upgrade collective.cover (closes `#225`_).
  [winstonf88]

* Corrige conteúdo inicial para novas versões do collective.cover (closes `#221`_, `#229`_).
  [rodfersou, winstonf88]


1.1.2 (2015-09-18)
^^^^^^^^^^^^^^^^^^

* Executa upgrade das dependências do brasil.gov.portal (closes `#218`_).
  [winstonf88]

* Corrige conteúdo inicial para novas versões do collective.cover (closes `#216`_).
  [rodfersou, winstonf88]

* Todas as pastas da raiz precisam ter a ordenação padrão do Plone (closes `#190`_).
  [idgserpro]


1.1.1 (2015-09-04)
2.0a1 (unreleased)
^^^^^^^^^^^^^^^^^^

- Nothing changed yet.


Previous entries can be found in the HISTORY.rst file.
