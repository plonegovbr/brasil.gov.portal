*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/annotate.robot
Resource  brasil/gov/portal/tests/robot/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Abrir navegador
Test Teardown  Fechar todos os navegadores


*** Variables ***

${tuser-pode-adicionar-td}    div[@id='user-group-sharing-container']/table/tbody/tr[2]/td[2]
${id-pasta-teste}             teste


*** Test Cases ***

Scenario: Habilitar Compartilhamento Local
    autenticar como administrador do site
    criar uma pasta de teste
    acessar a aba compartilhamento da pasta de teste
    pesquisar pelo usuario de teste
    conceder a permissão pode adicionar
    # recarregar a pagina
    acessar a aba compartilhamento da pasta de teste
    permissao deve ser local e nao um valor herdado


*** Keywords ***

autenticar como administrador do site
    Enable Autologin as    Site Administrator

criar uma pasta de teste
    Go To    ${PLONE_URL}/++add++Folder
    Input Text For Sure    form.widgets.IDublinCore.title    ${id-pasta-teste}
    Click Button    name=form.buttons.save
    Wait Until Page Contains    Item criado

acessar a aba compartilhamento da pasta de teste
    Go To    ${PLONE_URL}/${id-pasta-teste}/@@sharing
    Wait Until Page Contains    Compartilhamento para ${id-pasta-teste}

pesquisar pelo usuario de teste
    Input Text For Sure    sharing-user-group-search    test-user
    Wait Until Page Contains Element    xpath=//td[@title='test_user_1_']

conceder a permissão pode adicionar
    Select Checkbox    xpath=//${tuser-pode-adicionar-td}/input
    Click Button    name=form.button.Save
    Wait Until Page Contains    salvas

permissao deve ser local e nao um valor herdado
    Capture Page Screenshot    compartilhamento-usuarios.png
    Page Should Contain Element    xpath=//${tuser-pode-adicionar-td}/input[@checked='checked']
    Page Should Not Contain Element    xpath=//${tuser-pode-adicionar-td}/img
