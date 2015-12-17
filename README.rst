*******************************************************************
.gov.br: Portal Padrão da Identidade Digital do Governo
*******************************************************************

.. contents:: Conteúdo
   :depth: 2

Introdução
----------

Este pacote provê configurações para implementação da Identidade Digital de Governo em sites Plone do Governo da República Federativa do Brasil.

O desenvolvimento deste pacote foi feito como parte da iniciativa `Portal Padrão <http://portalpadrao.plone.org.br>`_ da comunidade `PloneGov.Br <http://www.softwarelivre.gov.br/plone>`_.

Requisitos
----------

Para uso deste pacote, seu site deve ter sido construído com:

    * Plone 4.3.3
    * Pinagem correta das `dependências <https://github.com/plonegovbr/brasil.gov.portal/blob/master/setup.py#L45>`_ do ``brasil.gov.portal``: cada release possui um ``versions.cfg`` específico em `portalpadrao.release <https://github.com/plonegovbr/portalpadrao.release>`_. Utilize o ``versions.cfg`` correspondente ao release de ``brasil.gov.portal`` utilizado.

Recomendamos a leitura do `documento <http://identidade-digital-de-governo-plone.readthedocs.org/en/latest/>`_ sobre a instalação deste pacote.

Estado deste pacote
-------------------

O **brasil.gov.portal** tem testes automatizados e, a cada alteração em seu
código os testes são executados pelo serviço Travis.

O estado atual dos testes, a cobertura de código e o número de downloads deste pacote podem ser vistos nas imagens a seguir:

.. image:: http://img.shields.io/pypi/v/brasil.gov.portal.svg
    :target: https://pypi.python.org/pypi/brasil.gov.portal

.. image:: https://img.shields.io/pypi/dm/brasil.gov.portal.svg
    :target: https://pypi.python.org/pypi/brasil.gov.portal

.. image:: https://img.shields.io/travis/plonegovbr/brasil.gov.portal/master.svg
    :target: http://travis-ci.org/plonegovbr/brasil.gov.portal

.. image:: https://img.shields.io/coveralls/plonegovbr/brasil.gov.portal/master.svg
    :target: https://coveralls.io/r/plonegovbr/brasil.gov.portal

Instalação
----------

Para habilitar a instalação deste produto em um ambiente que utilize o
buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e
   adicionar o pacote ``brasil.gov.portal`` à lista de eggs da instalação::

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

Sobrescrita de traduções do domínio plone
-----------------------------------------

Se você tem um produto que tem como dependência o brasil.gov.portal e precisa sobrescrever traduções do domínio plone nesse produto, sua diretiva ```<i18n:registerTranslations directory="locales" />``` deve vir antes da diretiva ```<includeDependencies package="." />```, ou de qualquer outra diretiva que carrege o ZCML do brasil.gov.portal. O seu configure.zcml deve ficar assim:
::
    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:i18n="http://namespaces.zope.org/i18n"
        i18n_domain="meu.produto">

      <i18n:registerTranslations directory="locales" />

      <includeDependencies package="." />
      
      ...
   </configure>

O ZCML do brasil.gov.porta carrega o ZCML do Products.CMFPlone, que por sua vez carrega o ZCML do plone.app.locales. Assim o locales do seu produto precisa ser carregado antes do ZCML do  brasil.gov.portal para que as traduções do seu produto possam sobrescrever às do Plone.

5. Adicione um novo site Plone.
O ZCML do brasil.gov.porta carrega o ZCML do Products.CMFPlone, que por sua vez carrega o ZCML do plone.app.locales. Assim o locales do seu produto precisa ser carregado antes do ZCML do  brasil.gov.portal para que as traduções do seu produto possam sobrescrever às do Plone.
