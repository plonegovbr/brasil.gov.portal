*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/annotate.robot
Resource  brasil/gov/portal/tests/robot/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Abrir navegador
Test Teardown  Fechar todos os navegadores


*** Variables ***

${tuser-pode-adicionar-td}    div[@id='user-group-sharing-container']/table/tbody/tr[2]/td[2]


*** Test Cases ***

Scenario: Habilitar Compartilhamento Local
    autenticar como administrador do site
    acessar a aba compartilhamento da pasta assuntos
    pesquisar pelo usuario de teste
    conceder a permissão pode adicionar
    # recarregar a pagina
    acessar a aba compartilhamento da pasta assuntos
    permissao deve ser local e nao um valor herdado


*** Keywords ***

autenticar como administrador do site
    Enable Autologin as    Site Administrator

acessar a aba compartilhamento da pasta assuntos
    Go To    ${PLONE_URL}/assuntos/@@sharing
    Wait Until Page Contains    Compartilhamento para Assuntos

pesquisar pelo usuario de teste
    Input Text For Sure    sharing-user-group-search    test-user
    Wait Until Page Contains Element    xpath=//td[@title='test_user_1_']

conceder a permissão pode adicionar
    Select Checkbox    xpath=//${tuser-pode-adicionar-td}/input
    Click Button                name=form.button.Save
    Wait Until Page Contains    salvas

permissao deve ser local e nao um valor herdado
    Capture Page Screenshot    compartilhamento-usuarios.png
    Page Should Contain Element    xpath=//${tuser-pode-adicionar-td}/input[@checked='']
    Page Should Not Contain Element    xpath=//${tuser-pode-adicionar-td}/img
