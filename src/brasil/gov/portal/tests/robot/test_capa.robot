*** Settings ***

Resource  brasil/gov/portal/tests/robot/keywords.robot
Resource  collective/cover/tests/cover.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Abrir navegador
Test Teardown  Fechar todos os navegadores

*** Variables ***

${banner_tile_location}  'collective.cover.banner'
${tile_selector}  div.tile-container div.tile
${document_selector}  .ui-draggable .contenttype-document

*** Keywords ***
# Metodo retirado do teste cover.robot do collective.cover para sobrescrever a chamada
# deste metodo aqui no test_capa.robot, esta customização é necessária pois temos que inserir
# Input Text For Sure para que o teste execute sem erros no travis
# FIXME: essa customização já foi realizada no produto collective.cover:
# https://github.com/collective/collective.cover/commit/dfd128a1ca6a75edc5f5190919bcffe7c9b4182f
# A customização pode ser removida quando utilizarmos o collective.cover versão > 1.2b1
Create Cover
    [arguments]  ${title}  ${description}  ${layout}=Empty layout

    Click Add Cover
    # deal with delays caused by plone4.csrffixes
    Input Text For Sure  css=${title_selector}  ${title}
    Input Text  css=${description_selector}  ${description}
    Select From List  css=${layout_selector}  ${layout}
    Click Button  Save
    Page Should Contain  Item created

*** Test Cases ***

Criar nova capa

    # Todos os keywords de collective.cover têm como premissa as strings em
    # inglês na interface.
    # Como os testes de brasil.gov.portal são em português, existiam duas
    # formas de aproveitar os keywords de collective.cover:
    # 1 - Customizando os keywords, aqui nesse arquivo, mas aí alterações que
    # fossem feitas futuramente lá teriam de ser replicadas aqui;
    # 2 - Setar o site em inglês apenas para esse teste.
    # A longo prazo, é mais vantajoso setar o site em inglês, por envolver
    # menos customização e não impactar os demais testes.
    Enable Autologin as  Site Administrator
    Ir para  ${PLONE_URL}/@@language-controlpanel
    Select From List  xpath=//select[@id='form.default_language']  en
    Clicar botao  Salvar

    # Cria a capa Layout vazio
    Go to Homepage
    Create Cover  NewCoverLayoutVazio  NewCoverLayoutVazioDescription  Layout vazio

    # Adiciona um tile de banner
    Open Layout Tab
    Add Tile  ${banner_tile_location}
    Save Cover Layout

    # Vê a mensagem padrão
    Compose Cover
    Page Should Contain   Drag&drop an image or link here to populate the tile

    # Arraste e solte um documento
    Open Content Chooser
    Drag And Drop  css=${document_selector}  css=${tile_selector}
    Wait Until Page Contains Element  css=div.cover-banner-tile

    # Move para a visão padrão
    Click Link  link=View
    # Na estrutura atual, provavelmente vai pegar o item "Acessibilidade"
    # Se novos tipos padrão de conteúdo inicial forem adicionados
    # em brasil.gov.portal, esse xpath pode ter que mudar para referenciar
    # outro documento.
    Wait Until Page Contains Element  xpath=//div[contains(@class, 'cover-banner-tile tile-content')]/h2/a[contains(@href, "acessibilidade")]

    # Cria a capa Destaques
    Go to Homepage
    Create Cover  NewCoverDestaques  NewCoverDestaquesDescription  Destaques

    # Vê a mensagem padrão
    Compose Cover
    Page Should Contain   Please add up to 5 objects to the tile

    # Arraste e solte um documento
    Open Content Chooser
    Drag And Drop  css=${document_selector}  css=${tile_selector}
    Wait Until Page Contains Element  css=ul.cover-list-tile

    # Move para a visão padrão
    Click Link  link=View
    # Na estrutura atual, provavelmente vai pegar o item "Acessibilidade"
    # Se novos tipos padrão de conteúdo inicial forem adicionados
    # em brasil.gov.portal, esse xpath pode ter que mudar para referenciar
    # outro documento.
    Wait Until Page Contains Element  xpath=//div[@id='em-destaque']/ul[contains(@class, 'sortable-tile cover-list-tile')]/li/a[contains(@href, "acessibilidade")]
