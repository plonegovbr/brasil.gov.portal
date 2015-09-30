Histórico de Alterações
-------------------------

1.1.3 (unreleased)
^^^^^^^^^^^^^^^^^^

* Reindexa capas para corrigir erro de consulta no catalog. (closes `#226`_).
  [winstonf88]

* Adiciona Products.PloneHotfix20150910 como dependência do pacote. (closes `#232`_)
  Ver: https://pypi.python.org/pypi/Products.PloneHotfix20150910
  [idgserpro]

* Corrige a execução do upgrade collective.cover. (closes `#225`_)
  [winstonf88]

* Corrige conteúdo inicial para novas versões do collective.cover. (closes `#221`_ `#229`_).
  [rodfersou, winstonf88]


1.1.2 (2015-09-18)
^^^^^^^^^^^^^^^^^^

* Executa upgrade das dependências do brasil.gov.portal. (closes `#218`_).
  [winstonf88]

* Corrige conteúdo inicial para novas versões do collective.cover. (closes `#216`_).
  [rodfersou, winstonf88]

* Todas as pastas da raiz precisam ter a ordenação padrão do Plone. (closes `#190`_).
  [idgserpro]


1.1.1 (2015-09-04)
^^^^^^^^^^^^^^^^^^

- Corrige release quebrado.
  [hvelarde]


1.1 (2015-09-03)
^^^^^^^^^^^^^^^^

* Desabilitando o item "Configurações do Site" do header do site.
  Ver issue https://github.com/plonegovbr/brasil.gov.portal/issues/212.
  [winstonf88]

* Adicionando meta tag creator.productor para contexto do link de Serviços da
  barra conforme manual. Ver item 2 de http://barra.governoeletronico.gov.br/
  [caduvieira]

* Corrige erro do rodapé que exibia link e sessões não publicadas. Para isso,
  forçamos Products.Doormat > 0.7 (closes `#182`_).
  [idgserpro]

* Reduzindo tamanho das imagens pelo tinypng. Taxa de redução foi de 59% do total.
  [caduvieira]

* Adiciona "memoize" na renderização de viewlet byline do NITF por questões de
  performance quando há muitos usuários sendo pesquisados.
  Ver https://github.com/collective/collective.nitf/pull/129
  [idgserpro]

* Adiciona css para title de coleção.
  [idgserpro]

* Corrige as dependências do pacote.
  [hvelarde]

* Adiciona viewlets internacionalizadas (i18n) para "Voltar para o topo",
  "Desenvolvido com o CMS de código aberto Plone" e os links de acessibilidade
  para evitar que brasil.gov.temas tenha de ser customizado quando outra
  língua for adicionada.
  [idgserpro]
* Corrige css de impressão, colocando texto como justificado. Alguns documentos
  oficiais que são impressos nos portais estão tendo problemas em juntas
  comerciais por não estarem com o texto alinhado na forma "justificada". `#161`_
  [idgserpro]
* Viabiliza uso de "tachado" e "sublinhado" no editor. (closes `#175`_)
  [idgserpro]
* Adiciona brasil.gov.portlets como dependência de Portal Padrão.
  [dbarbato]
* Corrige bug em paginação na visão de galeria de álbuns.
  [dbarbato]


1.0.5 (2014-12-05)
^^^^^^^^^^^^^^^^^^
* Adiciona ao code-analysis Flake8, Deprecated aliases, Check utf-8 headers,
  Check clean lines, Double quotes e Check imports
  [dbarbato]
* Adiciona internacionalização para templates e scripts.
  [dbarbato]
* Adiciona estilos para portlet Centrais de Conteúdos em inglês e espanhol.
  [dbarbato]
* Ajusta para alterar estilo da primeira navegação apenas quando título for
  Menu de relevância.
  [dbarbato]
* Adiciona sprite e estilo de contraste para ícone de Dados Abertos do menu
  de Centrais de Conteúdos.
  [dbarbato]


1.0.4 (2014-11-01)
^^^^^^^^^^^^^^^^^^
* Altera página inicial após instalação do pacote.
  [ericof]
* Altera página de criação de sites.
  [ericof]
* Adiciona versão do Portal Padrão à página do Painel de controle.
  [ericof]
* Corrige css de impressão. (closes `#161`_)
  [idgserpro]
* Corrige versão do metadata.xml. (closes `#173`_)
  [idgserpro]
* Ajusta bug no popup do Products.TinyMCE que impedia de selecionar um item
  para se tornar link. (closes `#159`_)
  [idgserpro]
* Ajusta bug de coleções.
  [dbarbato]
* Inverte ícones de publicações e infográficos de central de conteúdos.
  [dbarbato]
* Acertos nos testes.
  [dbarbato]
* Acertos de Flake8.
  [dbarbato]


1.0.3 (2014-06-11)
^^^^^^^^^^^^^^^^^^
* Uso do plone.api
  [ericof]
* Corrige contraste dos botões do menu responsivo
  [dbarbato]
* Corrige permissão do painel de controle de redes sociais
  [ericof]
* Corrige contraste do campo de busca do header
  [dbarbato]
* Corrige factory dos tipos internos de Áudio
  [ericof]
* brasil.sections.jsonsource agora suporta variáveis de ambiente para passagem de parâmetro.
  [ericof]
* Ajusta CSS de contraste.
  [dbarbato]
* Ajusta nome de tipo de item na visão sumária de pasta.
  [dbarbato]


1.0.2.1 (2014-03-11)
^^^^^^^^^^^^^^^^^^^^^^

* Ajusta tempo de execução de javascript na view de álbuns.
  [dbarbato]
* Cria passo de atualização para ordenação de pastas
  [ericof]

1.0.2 (2014-02-28)
^^^^^^^^^^^^^^^^^^
* Registra view de álbuns no profile default (close `#152`_).
  [rodfersou]
* Adiciona ícones de redes sociais tumblr e instagram (closes `#150`_).
  [rodfersou][rennanrodrigues]
* Ajusta estilo do Menu de idiomas.
  [dbarbato]
* Ajusta novo tile de galeria de álbuns (close `#141`_).
  [rodfersou]
* Remove o termo Pasta para Pasta/Álbum na página de busca.
  (closes `#148`_).
  [dbarbato]
* Adiciona brasil.gov.agenda como dependência e registra tile de Agenda.
  [dbarbato]
* Ajusta alinhamento em páginas onde tem legenda de imagens à
  esquerda (closes `#143`_).
  [dbarbato]
* Remove não ordenação de pastas do conteúdo inicial (closes `#136`_).
  [dbarbato]
* Altera definição de cor dos ícones da navegação sumária para as 4 cores
  no produto de temas (closes `#132`_).
  [felipeduardo]
* Adicionada novas visualizações para pasta de imagens -
  Galeria de álbuns e Galeria de fotos (closes `#130`_).
  [rodfersou]
* Altera o termo Pasta para Pasta/Álbum na página de busca.
  [rodfersou]
* Adiciona o campo Direitos no upload múltiplo de imagens. (closes `#128`_).
  [rodfersou]


1.0.1 (2013-12-12)
^^^^^^^^^^^^^^^^^^^
* Adicionamos o Products.PloneHotfix20131210 como dependência do portal.
  [ericof]
* Adiciona o brasil.gov.agenda ao portal padrão.
  [ericof]
* Visão sumária de pasta deve ser igual a visão sumária de coleções
  (closes `#118`_).
  [rodfersou]
* Correções de contraste (closes `#38`_).
  [rodfersou]
* Definindo altura minima para visualizar Social Like.
  [dbarbato]
* Generalizando regras de tamanho dos botoes do Social Like.
  [dbarbato]
* Implementação de comportamento dinamico na altura do breadcrumb (closes `#111`_).
  [felipeduardo]
* Correções de tamanhos de títulos nos tiles (closes `#106`_).
  [rodfersou]
* Implementação de CSS para modo de alto contraste em tiles que não tinham
  essa opção (closes `#38`_).
  [felipeduardo]
* Melhorias de estilo no mapa do site (closes `#104`_).
  [rodfersou]
* Aumentada fonte do menu site actions (closes `#102`_).
  [rodfersou]
* Aumentada fonte do menu de acessibilidade (closes `#100`_).
  [rodfersou]
* Adicionada informação "voce está aqui" no breadcrumbs (closes `#98`_).
  [rodfersou]
* Revisado funcionamento do viewlet de detaques (closes `#96`_).
  [rodfersou]
* Removido patch para replicar alterações de autores para objetos filhos em
  tipos de dados Folderish.
  [dbarbato]
* Correção nas reticencias no inicio da paginação padrão do Plone, quando a
  página atual for um número alto (closes `#93`_).
  [rodfersou]
* Criado patch para replicar alterações de autores para objetos filhos em
  tipos de dados Folderish (closes `#90`_).
  [rodfersou]
* Regras dos Tiles de Redes sociais deletadas deste produto (closes `#88`_).
  [rennanrodrigues]


1.0 (2013-10-29)
^^^^^^^^^^^^^^^^^^^
* Regras de summary view adicionadas para navegação facetada (closes `#84`_).
  [rennanrodrigues]
* Correção em tamanho das imagens e espaçamentos na summary view de coleção (closes `#82`_).
  [rennanrodrigues]
* Correções de espaçamento no tipo de conteúdo NITF (closes `#80`_).
  [rennanrodrigues]
* Adicionado icones para os botões de impressão (closes `#78`_).
  [felipeduardo]
* Correção de registro de fonte no css (closes `#76`_).
  [rennanrodrigues]
* Novos ícones das redes sociais (closes `#74`_).
  [rennanrodrigues]


1.0rc2 (2013-10-24)
^^^^^^^^^^^^^^^^^^^
* Revisão da paginação padrão do plone (closes `#72`_).
  [rodfersou]
* Removidas as regras de css para os tiles, deixando apenas as definições para o contraste
  (closes `#70`_).
  [rennanrodrigues]
* Revisão de css do botão relatar erros (closes `#69`_).
  [rennanrodrigues]
* Correção em espaçamentos dos sub-itens do menu lateral esquerda (closes `#66`_).
  [felipeduardo]
* Corrigido caminho das referências css para funcionar em produção (closes `#64`_).
  [rodfersou]
* Customizada css de paginação padrão do plone
  Inserção de ícones na summary view de coleção
  Inserção de ícones na summary view de coleção no modo contraste
  Revisão de layout conforme arte (closes `#57`_).
  [rennanrodrigues]
* Movidas alterações de css da home que estavam no tema para estrutura principal
  de css. (closes `#60`_).
  [felipeduardo]
* CSS do icone de relatar erros (closes `#59`_).
  [rennanrodrigues]
* Customizada view de paginação padrão do plone
  Customização do template da summary view para inserir ícones (closes `#57`_).
  [rodfersou]
* Correção nos espaçamentos do menu da lateral esquerda (closes `#55`_).
  [felipeduardo]
* Movido implementação que havia ficado no produto de tema e alterado sintaxe
  padrão do arquivo javascript (closes `#46`_).
  [felipeduardo]
* Correção da img de sprites para centrais de conteudo, icone de busca, icones
  de central de conteudo em modo de alto contraste, renomeados icones das setas
  seguindo o nome da cor ao inves da editoria. (closes `#51`_).
  [felipeduardo]
* Movido tipo de dados conteúdo externo do portal brasil para portal modelo
  (closes `#49`_).
  [rodfersou]
* Correção em modo de alto contraste para os temas amarelo e branco (closes `#38`_).
  [felipeduardo]
* Revisão dos ícones de redes sociais (closes `#44`_).
  [rodfersou]
* Movido arquivo javascript dos temas para brasil.gov.portal (closes `#46`_).
  [rodfersou]
* Padronização no espaçamento entre o menu de navegação e do conteudo principal
  quando em três colunas. (closes `#40`_).
  [felipeduardo]
* Ajuste no alinhamento do menu de navegação e do conteudo principal (closes `#40`_).
  [felipeduardo]
* AJuste no CSS em modo de Alto Contraste para manter a barra de identidade
  com as cores padrões. (closes `#38`_).
  [felipeduardo]
* AJuste no CSS em modo de Alto Contraste (closes `#38`_).
  [felipeduardo]
* Revisão de ícones de redes sociais para escolher cor por tema (closes `#35`_).
  [rodfersou]
* Movido main.css do brasil.gov.temas para brasil.gov.portal.
  Será mantido no tema somente para previsualizacao do tema (closes `#34`_).
  [rodfersou]
* Remoção de estilos inline (closes `#32`_).
  [rennanrodrigues]
* Customizada viewlet plone.analytics para ter uma div em torno de seu conteúdo,
  possibilitando mapeamento no Diazo (closes `#30`_).
  [rodfersou]
* Movidas customizacoes nitf do portal brasil para portal modelo (closes `#26`_).
  [rodfersou]
* Removidas customizações da pasta overrides to tema, e movidas para brasil.gov.portal
  (closes `#19`_).
  [rodfersou]
* Customizado template do breadcrumb para ficar igual ao layout sugerido (closes `#17`_).
  [rodfersou]
* Fix related itens viewlet exception (closes `#21`_).
  [rodfersou]
* Criação de nova classe css para tiles cover e upgrade step (closes `#14`_).
  [rodfersou]
* Remoção do link no nome do autor após titulo (closes `#10`_).
  [felipeduardo]
* Alteração textual no legend da pagina de busca (closes `#7`_) [felipeduardo]
  [felipeduardo]


1.0rc1 (2013-08-26)
^^^^^^^^^^^^^^^^^^^
* Atividade 320: Ajuste Estilo - Listagem Vertical [rennanrodrigues]
* Atividade 324: Acertos na Busca [rodfersou]
* Inserindo virgulas entre as tags - summary view  [dbarbato]
* Exibir data efetiva no lugar da de modificacao - summary view [dbarbato]
* Ocultados alguns profiles de upgrades. [ericof]
* Adicionada verificação para não incluir home caso já existir na
  rotina de conteúdo inicial do portal. [ericof]


1.0a1 (2013-07-22)
^^^^^^^^^^^^^^^^^^
* Versão inicial do pacote [ericof]


.. _`#7`: https://github.com/plonegovbr/brasil.gov.portal/issues/7
.. _`#10`: https://github.com/plonegovbr/brasil.gov.portal/issues/10
.. _`#14`: https://github.com/plonegovbr/brasil.gov.portal/issues/14
.. _`#17`: https://github.com/plonegovbr/brasil.gov.portal/issues/17
.. _`#19`: https://github.com/plonegovbr/brasil.gov.portal/issues/19
.. _`#21`: https://github.com/plonegovbr/brasil.gov.portal/issues/21
.. _`#26`: https://github.com/plonegovbr/brasil.gov.portal/issues/26
.. _`#30`: https://github.com/plonegovbr/brasil.gov.portal/issues/30
.. _`#34`: https://github.com/plonegovbr/brasil.gov.portal/issues/34
.. _`#35`: https://github.com/plonegovbr/brasil.gov.portal/issues/35
.. _`#32`: https://github.com/plonegovbr/brasil.gov.portal/issues/32
.. _`#38`: https://github.com/plonegovbr/brasil.gov.portal/issues/38
.. _`#40`: https://github.com/plonegovbr/brasil.gov.portal/issues/40
.. _`#44`: https://github.com/plonegovbr/brasil.gov.portal/issues/44
.. _`#46`: https://github.com/plonegovbr/brasil.gov.portal/issues/46
.. _`#49`: https://github.com/plonegovbr/brasil.gov.portal/issues/49
.. _`#51`: https://github.com/plonegovbr/brasil.gov.portal/issues/51
.. _`#55`: https://github.com/plonegovbr/brasil.gov.portal/issues/55
.. _`#57`: https://github.com/plonegovbr/brasil.gov.portal/issues/57
.. _`#59`: https://github.com/plonegovbr/brasil.gov.portal/issues/59
.. _`#60`: https://github.com/plonegovbr/brasil.gov.portal/issues/60
.. _`#64`: https://github.com/plonegovbr/brasil.gov.portal/issues/64
.. _`#66`: https://github.com/plonegovbr/brasil.gov.portal/issues/66
.. _`#69`: https://github.com/plonegovbr/brasil.gov.portal/issues/69
.. _`#70`: https://github.com/plonegovbr/brasil.gov.portal/issues/70
.. _`#72`: https://github.com/plonegovbr/brasil.gov.portal/issues/72
.. _`#74`: https://github.com/plonegovbr/brasil.gov.portal/issues/74
.. _`#76`: https://github.com/plonegovbr/brasil.gov.portal/issues/76
.. _`#78`: https://github.com/plonegovbr/brasil.gov.portal/issues/78
.. _`#80`: https://github.com/plonegovbr/brasil.gov.portal/issues/80
.. _`#82`: https://github.com/plonegovbr/brasil.gov.portal/issues/82
.. _`#84`: https://github.com/plonegovbr/brasil.gov.portal/issues/84
.. _`#88`: https://github.com/plonegovbr/brasil.gov.portal/issues/88
.. _`#90`: https://github.com/plonegovbr/brasil.gov.portal/issues/90
.. _`#93`: https://github.com/plonegovbr/brasil.gov.portal/issues/93
.. _`#96`: https://github.com/plonegovbr/brasil.gov.portal/issues/96
.. _`#98`: https://github.com/plonegovbr/brasil.gov.portal/issues/98
.. _`#100`: https://github.com/plonegovbr/brasil.gov.portal/issues/100
.. _`#102`: https://github.com/plonegovbr/brasil.gov.portal/issues/102
.. _`#104`: https://github.com/plonegovbr/brasil.gov.portal/issues/104
.. _`#106`: https://github.com/plonegovbr/brasil.gov.portal/issues/106
.. _`#111`: https://github.com/plonegovbr/brasil.gov.portal/issues/111
.. _`#118`: https://github.com/plonegovbr/brasil.gov.portal/issues/118
.. _`#128`: https://github.com/plonegovbr/brasil.gov.portal/issues/128
.. _`#130`: https://github.com/plonegovbr/brasil.gov.portal/issues/130
.. _`#132`: https://github.com/plonegovbr/brasil.gov.portal/issues/132
.. _`#136`: https://github.com/plonegovbr/brasil.gov.portal/issues/136
.. _`#141`: https://github.com/plonegovbr/brasil.gov.portal/issues/141
.. _`#143`: https://github.com/plonegovbr/brasil.gov.portal/issues/143
.. _`#148`: https://github.com/plonegovbr/brasil.gov.portal/issues/148
.. _`#150`: https://github.com/plonegovbr/brasil.gov.portal/issues/150
.. _`#152`: https://github.com/plonegovbr/brasil.gov.portal/issues/152
.. _`#159`: https://github.com/plonegovbr/brasil.gov.portal/issues/159
.. _`#161`: https://github.com/plonegovbr/brasil.gov.portal/issues/161
.. _`#173`: https://github.com/plonegovbr/brasil.gov.portal/issues/173
.. _`#175`: https://github.com/plonegovbr/brasil.gov.portal/issues/175
.. _`#182`: https://github.com/plonegovbr/brasil.gov.portal/issues/182
.. _`#190`: https://github.com/plonegovbr/brasil.gov.portal/issues/190
.. _`#216`: https://github.com/plonegovbr/brasil.gov.portal/issues/216
.. _`#218`: https://github.com/plonegovbr/brasil.gov.portal/issues/218
.. _`#221`: https://github.com/plonegovbr/brasil.gov.portal/issues/221
.. _`#225`: https://github.com/plonegovbr/brasil.gov.portal/issues/225
.. _`#226`: https://github.com/plonegovbr/brasil.gov.portal/issues/226
.. _`#229`: https://github.com/plonegovbr/brasil.gov.portal/issues/229
.. _`#232`: https://github.com/plonegovbr/brasil.gov.portal/issues/232
