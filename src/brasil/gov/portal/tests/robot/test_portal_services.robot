*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/annotate.robot
Resource  brasil/gov/portal/tests/robot/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Abrir navegador
Test Teardown  Fechar todos os navegadores


*** Test Cases ***

Adicionar link no portal services
    Como o usuario administrador  Machado de Assis
    Ir para  ${PLONE_URL}/@@portal-services-settings

    ${csrf} =  Run keyword and return status
    ...  Pagina deve conter  Confirmando Ação do Usuário.
    Run keyword if  ${csrf}
    ...  Clicar botao  Confirmar ação

    Sleep  2s
    Clicar botao  Adicionar Link
    Campo de texto  form.widgets.title  Fale Conosco
    Campo de texto  form.widgets.description  Link para o Fale Conosco
    Campo de texto  form.widgets.url_expr  /fale-conosco
    Clicar botao  Adicionar

    Ir para  ${PLONE_URL}/@@portal-services-settings
    Pagina deve conter  Fale Conosco

Editar o link
    Como o usuario administrador  Machado de Assis
    Ir para  ${PLONE_URL}/@@portal-services-settings

    ${csrf} =  Run keyword and return status
    ...  Pagina deve conter  Confirmando Ação do Usuário.
    Run keyword if  ${csrf}
    ...  Clicar botao  Confirmar ação

    Sleep  2s
    Clicar botao  Adicionar Link
    Campo de texto  form.widgets.title  Fale Conosco
    Campo de texto  form.widgets.description  Link para o Fale Conosco
    Campo de texto  form.widgets.url_expr  /fale-conosco
    Clicar botao  Adicionar

    Click Link  css=.controlpanel-listing td>a
    Campo de texto  form.widgets.title  Participe
    Campo de texto  form.widgets.description  Link para Participe
    Campo de texto  form.widgets.url_expr  /participe
    Clicar botao  Salvar

    Ir para  ${PLONE_URL}/@@portal-services-settings
    Pagina deve conter  Participe

Remover o link
    Como o usuario administrador  Machado de Assis
    Ir para  ${PLONE_URL}/@@portal-services-settings

    ${csrf} =  Run keyword and return status
    ...  Pagina deve conter  Confirmando Ação do Usuário.
    Run keyword if  ${csrf}
    ...  Clicar botao  Confirmar ação

    Sleep  2s
    Clicar botao  Adicionar Link
    Campo de texto  form.widgets.title  Fale Conosco
    Campo de texto  form.widgets.description  Link para o Fale Conosco
    Campo de texto  form.widgets.url_expr  /fale-conosco
    Clicar botao  Adicionar

    Ir para  ${PLONE_URL}/@@portal-services-settings
    Pagina deve conter  Fale Conosco
    Clicar botao  Excluir
    Page Should Not Contain  Fale Conosco

