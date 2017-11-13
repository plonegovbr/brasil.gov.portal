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
    Wait Until Page Contains Element  xpath=//select[@id='form.default_language']
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
