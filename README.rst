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
