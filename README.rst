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

    * Plone 4.3.3 ou superior (http://plone.org/products/plone)

Recomendamos a leitura do `documento <http://identidade-digital-de-governo-plone.readthedocs.org/en/latest/>`_ sobre instalação deste pacote.

Estado deste pacote
-------------------

O **brasil.gov.portal** tem testes automatizados e, a cada alteração em seu
código os testes são executados pelo serviço Travis. 

O estado atual dos testes, a cobertura de código e o número de downloads deste pacote podem ser vistos nas imagens a seguir:

.. image:: https://secure.travis-ci.org/plonegovbr/brasil.gov.portal.png?branch=master
    :target: http://travis-ci.org/plonegovbr/brasil.gov.portal
    
.. image:: https://coveralls.io/repos/plonegovbr/brasil.gov.portal/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/plonegovbr/brasil.gov.portal

.. image:: https://pypip.in/d/brasil.gov.portal/badge.png
    :target: https://pypi.python.org/pypi/brasil.gov.portal/
    :alt: Downloads

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

2. Após alterar o arquivo de configuração é necessário executar
   ''bin/buildout'', que atualizará sua instalação.

3. Reinicie o Plone

4. Adicione um novo site Plone.
