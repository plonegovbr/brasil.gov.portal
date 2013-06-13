*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/annotate.robot
Resource  brasil/gov/portal/tests/robot/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Abrir navegador
Test Teardown  Fechar todos os navegadores


*** Test Cases ***

Site com titulo curto
    Como o usuario administrador  Machado de Assis
    Ir para  ${PLONE_URL}/@@site-controlpanel
    Campo de texto  form.site_title_1  Ministerio
    Campo de texto  form.site_title_2  da Cultura
    Campo de texto  form.site_orgao  Presidencia da Republica
    Campo de texto  form.site_description  Site da SECOM
    Clicar botao  Salvar

    Ir para  ${PLONE_URL}
    Pagina deve conter  Ministerio
    Pagina deve conter  da Cultura
    Capturar tela  site-titulo-curto.png

Site com titulo longo
    Como o usuario administrador  Machado de Assis
    Ir para  ${PLONE_URL}/@@site-controlpanel
    Campo de texto  form.site_title_1  Ministerio
    Campo de texto  form.site_title_2  Desenvolvimento Social e Combate a Fome
    Campo de texto  form.site_orgao  Presidencia da Republica
    Campo de texto  form.site_description  Site da SECOM
    Clicar botao  Salvar

    Ir para  ${PLONE_URL}
    Pagina deve conter  Ministerio
    Pagina deve conter  Desenvolvimento Social e Combate a Fome
    Capturar tela  site-titulo-longo.png


*** Keywords ***

Apenas o tipo Imagem deve ser listado
    Element should contain  plone-contentmenu-factories  Image
    Page Should Not Contain Element  css=dl#plone-contentmenu-factories a.event
    Page Should Not Contain Element  css=dl#plone-contentmenu-factories a.folder
    Page Should Not Contain Element  css=dl#plone-contentmenu-factories a.collection
    Page Should Not Contain Element  css=dl#plone-contentmenu-factories a.link
    Page Should Not Contain Element  css=dl#plone-contentmenu-factories a.document