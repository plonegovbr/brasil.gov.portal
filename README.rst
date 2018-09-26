*******************************************************
.gov.br: Portal Padrão da Identidade Digital do Governo
*******************************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
----------

Este complemento provê configurações para implementação da Identidade Digital de Governo em sites Plone do Governo da República Federativa do Brasil.

O desenvolvimento deste complemento foi feito como parte da iniciativa `Portal Padrão <http://portalpadrao.plone.org.br>`_ da comunidade `PloneGov.Br <http://www.softwarelivre.gov.br/plone>`_.

Requisitos
----------

Para uso deste complemento, seu site deve ter sido construído com:

* Plone 4.3.18
* Pinagem correta das `dependências <https://github.com/plonegovbr/brasil.gov.portal/blob/master/setup.py#L45>`_ do ``brasil.gov.portal``: cada release possui um ``versions.cfg`` específico em `portalpadrao.release <https://github.com/plonegovbr/portalpadrao.release>`_.

**Atenção**: Leia atentamente `a seção sobre como escolher o seu arquivo de versões de release <https://github.com/plonegovbr/portalpadrao.release/#user-content-como-escolher-corretamente-o-arquivo-de-versões-de-um-release>`_ para entender qual versão usar.

Recomendamos a leitura do `documento <http://identidade-digital-de-governo-plone.readthedocs.org/en/latest/>`_ sobre a instalação deste complemento.

Estado deste complemento
------------------------

O **brasil.gov.portal** tem testes automatizados e, a cada alteração em seu
código os testes são executados pelo serviço Travis.

O estado atual do complemento pode ser visto nas imagens a seguir:

.. image:: http://img.shields.io/pypi/v/brasil.gov.portal.svg
    :target: https://pypi.python.org/pypi/brasil.gov.portal

.. image:: https://img.shields.io/travis/plonegovbr/brasil.gov.portal/master.svg
    :target: http://travis-ci.org/plonegovbr/brasil.gov.portal

.. image:: https://img.shields.io/coveralls/plonegovbr/brasil.gov.portal/master.svg
    :target: https://coveralls.io/r/plonegovbr/brasil.gov.portal

.. image:: https://img.shields.io/codacy/grade/aa5a9980a6104e4390be5e6bc4f7460a.svg
    :target: https://www.codacy.com/project/plonegovbr/brasil.gov.portal/dashboard

Instalação
----------

Para habilitar a instalação deste complemento em um ambiente que utilize o buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e adicionar o complemento ``brasil.gov.portal`` à lista de eggs da instalação:

.. code-block:: cfg

      [buildout]
      ...
      eggs =
          brasil.gov.portal

2. Editar o arquivo ``buildout.cfg`` (ou outro arquivo de configuração)
   referenciando o uso do versions.cfg de acordo com o release presente em
   `portalpadrao.release <https://github.com/plonegovbr/portalpadrao.release>`_

3. Após alterar o arquivo de configuração é necessário executar
   ''bin/buildout'', que atualizará sua instalação.

4. Reinicie o Plone

5. Adicione um novo site Plone.

Atualização de 1.x a 2.x
------------------------

.. Warning::
    Só atualize para a versão 2.x do complemento depois de atualizar à versão mais recente da branch 1.x.

As atualizações da versão 1.x à 2.x só são suportadas das versões mais recentes de cada branch.
Antes de atualizar confira que você está efetivamente utilizando a última versão da branch 1.x e que não existem upgrade steps pendentes de serem aplicados.

Rodando o buildout de uma tag antiga do complemento
---------------------------------------------------

Para atender ao relato de ter vários jobs de integração contínua em complementos brasil.gov.* (ver https://github.com/plonegovbr/portalpadrao.release/issues/11), no fim da seção extends do buildout.cfg de todos os complementos brasil.gov.* temos a seguinte linha:

.. code-block:: cfg

    https://raw.githubusercontent.com/plonegovbr/portal.buildout/master/buildout.d/versions.cfg

Hoje, esse arquivo contém sempre as versões pinadas de um release a ser lançado. Por esse motivo, quando é feito o checkout de uma tag mais antiga provavelmente você não conseguirá rodar o buildout.
Dessa forma, após fazer o checkout de uma tag antiga, recomendamos que adicione, na última linha do extends, o arquivo de versões do IDG compatível com aquela tag, presente no repositório https://github.com/plonegovbr/portalpadrao.release/.

Exemplo: você clonou o repositório do brasil.gov.portal na sua máquina, e deu checkout na tag 1.0.5. Ao editar o buildout.cfg, ficaria dessa forma, já com a última linha adicionada:

.. code-block:: cfg

    extends =
        https://raw.github.com/collective/buildout.plonetest/master/test-4.3.x.cfg
        https://raw.github.com/collective/buildout.plonetest/master/qa.cfg
        http://downloads.plone.org.br/release/1.0.4/versions.cfg
        https://raw.githubusercontent.com/plonegovbr/portal.buildout/master/buildout.d/versions.cfg
        https://raw.githubusercontent.com/plone/plone.app.robotframework/master/versions.cfg
        https://raw.githubusercontent.com/plonegovbr/portalpadrao.release/master/1.0.5/versions.cfg

Para saber qual arquivo de versões é compatível, no caso do brasil.gov.portal, é simples pois é a mesma versão (no máximo um bug fix, por exemplo, brasil.gov.portal é 1.1.3 e o arquivo de versão é 1.1.3.1).
Para os demais complementos, recomendamos comparar a data da tag do complemento e a data nos changelog entre uma versão e outra para adivinhar a versão compatível.

Sobrescrita de traduções do domínio plone
-----------------------------------------

Se você tem um complemento que tem como dependência o brasil.gov.portal e precisa sobrescrever traduções do domínio ``plone`` nesse produto,
sua diretiva ``<i18n:registerTranslations directory="locales" />`` deve vir antes da diretiva ``<includeDependencies package="." />``,
ou de qualquer outra diretiva que carrege o ZCML do brasil.gov.portal.
O seu configure.zcml deve ficar assim:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        ...
        xmlns:i18n="http://namespaces.zope.org/i18n"
        i18n_domain="meu.produto">

      <i18n:registerTranslations directory="locales" />

      <includeDependencies package="." />

      ...

   </configure>

O ZCML do brasil.gov.portal carrega o ZCML do Products.CMFPlone, que por sua vez carrega o ZCML do plone.app.locales.
Assim o locales do seu produto precisa ser carregado antes do ZCML do  brasil.gov.portal para que as traduções do seu produto possam sobrescrever às do Plone.

Desenvolvimento
---------------

Utilizamos `webpack <https://webpack.js.org/>`_ para gerenciar o conteúdo estático do tema,
tomando vantagem das diversas ferramentas e plugins disponíveis para suprir nossas necessidades.

Utilizamos a receita de buildout `sc.recipe.staticresources <https://github.com/simplesconsultoria/sc.recipe.staticresources>`_ para integrar o `webpack`_ no Plone.

Ao desenvolver os temas iniciamos o watcher do `webpack`_ e trabalhamos somente na pasta "webpack" alterando os arquivos;
o `webpack`_ se encarrega de processar e gerar os arquivos em seu endereço final.

Este pacote adiciona os seguintes comandos na pasta bin do buildout para processar automaticamente os recursos estáticos:

.. code-block:: console

    $ bin/env-brasilgovportal

Este comando adiciona no terminal o node do buildout no PATH do sistema,
dessa forma voce pode trabalhar com webpack conforme a documentação oficial.

.. code-block:: console

    $ bin/watch-brasilgovportal

Este comando instrui ao `webpack`_ para esperar por qualquer mudança nos arquivos SASS e gera a versão minificada do CSS para a aplicação.

.. code-block:: console

    $ bin/debug-brasilgovportal

Este comando faz o mesmo que o comando watch, mas não minifica o CSS final.
Utilizado para debugar a geração do CSS.

.. code-block:: console

    $ bin/build-brasilgovportal

Este comando cria os recursos minificados, mas não espera por mudanças.

Fazendo releases com o zest.releaser
------------------------------------

Os recursos estáticos do pacote são gerados usando o `webpack`_ e não são inclusos no VCS.
Se você está fazendo release usando o zest.releaser, você precisa fazer `upload manual dos arquivos no PyPI <https://github.com/zestsoftware/zest.releaser/issues/261>`_ ou você vai criar uma distribuição quebrada:

* execute ``longtest``, como de costume
* execute ``fullrelease``, como de costume, respondendo "não" a pergunta "Check out the tag?" para evitar o upload ao PyPI
* faça checkout na tag do release que você está liberando
* execute ``bin/build-brasilgovportal`` para criar os recursos estáticos
* crie os arquivos da distribuição usando ``python setup.py sdist bdist_wheel``, como de costume
* faça o upload manual dos arquivos usando ``twine upload dist/*``

Em caso de erro você terá que criar um novo release pois o PyPI Warehouse `não permite reutilizar um nome de arquivo <https://upload.pypi.org/help/#file-name-reuse>`_.
