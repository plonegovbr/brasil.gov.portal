*** Settings ***

Resource  brasil/gov/portal/tests/robot/keywords.robot
Resource  collective/cover/tests/cover.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Abrir navegador
Test Teardown  Fechar todos os navegadores

*** Variables ***

${tile_location}  'collective.cover.richtext'
${edit_link_selector}  css=a.edit-tile-link
${pasta_exemplos}  xpath=//a[contains(@href, "pastas-com-exemplos-de-pecas")]
${exemplo_imagem}  xpath=//input[contains(@href, "/pastas-com-exemplos-de-pecas/foto-200-x-130.jpg")]


*** Test Cases ***

Criar banner destaque
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

    Ir para  ${PLONE_URL}/destaques/layoutedit
    Add Tile  ${tile_location}
    Save Cover Layout

    # FIXME: Por algum motivo, na build https://travis-ci.org/plonegovbr/brasil.gov.portal/builds/387898576#L1972
    # ocorre o erro por usar a keyword "Compose Cover". Essa keyword já é usada
    # em test_capa.robot e não dá problema. Em browsers mais novos (como 52.6.0esr)
    # esse erro não ocorre. Dessa forma, irei direto para a url "compose" com
    # outra keyword. Quando atualizarmos o browser nos testes, podemos voltar a
    # usar a keyword "Compose Cover" para manter a consistência de nomes.
    Ir para  ${PLONE_URL}/destaques/compose
    Page Should Contain   Please edit the tile to enter some text.

    Click Link  ${edit_link_selector}
    Wait Until Page Contains  Edit Rich Text Tile
    Sleep  1s  Wait for TinyMCE to load
    Wait For Condition  return typeof tinyMCE !== "undefined" && tinyMCE.activeEditor !== null && document.getElementById(tinyMCE.activeEditor.id) !== null
    Click Link  Insert/Edit Image
    Select frame  id=mce_inlinepopups_16_ifr
    Wait Until Page Contains Element  ${pasta_exemplos}
    Click Element  ${pasta_exemplos}
    # Clico aqui mudando a listagem para "lista" para facilitar a expressão abaixo.
    Click Link  css=a#listview
    # Seleciona o objeto resolveuid/896b6f9794fa4bfcac5cadbca080e33f
    Click Element  ${exemplo_imagem}
    Clicar botao  OK
    Unselect Frame
    Clicar botao  Save

    Ir para  ${PLONE_URL}

    Page Should Contain Element  css=div#featured-content div.row div div.tile div#em-destaque
    Page Should Contain Element  css=div#featured-content div.row div div.tile-default div.cover-richtext-tile
