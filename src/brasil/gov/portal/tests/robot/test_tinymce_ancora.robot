*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/annotate.robot
Resource  brasil/gov/portal/tests/robot/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Abrir navegador
Test Teardown  Fechar todos os navegadores


*** Test cases ***

Test Tinymce Ancora (Link Interno)

    Como o usuario administrador  Machado de Assis
    Ir para  ${PLONE_URL}/noticias/titulo-da-noticia-entre-35-e-90-caracteres-com-espaco/edit
    Wait Until Page Contains Element  id=form.widgets.text_ifr
    Select frame  id=form.widgets.text_ifr

    # Coloca um texto único para facilitar a manipulação da âncora.
    Input text  id=content  ANCORA
    Double Click Element  xpath=//body[@id='content']/p[1]

    # O botão de âncora está fora do iframe de texto, então preciso sair dele.
    Unselect Frame

    Click Link  css=span .mce_anchor

    # Preciso agora acessar outro iframe, o do popup de edição de ancora.
    Wait Until Page Contains Element  id=mce_inlinepopups_31_ifr
    Select frame  id=mce_inlinepopups_31_ifr
    Input text  id=anchorName  testeancora
    Click Button  Inserir

    # Preciso sair do frame do popup para selecionar o botão do conteúdo
    Unselect Frame

    Click Button  Salvar
    Page Should Contain Element  css=a[name="testeancora"]

    # Agora, em outro documento, iremos colocar a referência para essa âncora.

    Ir para  ${PLONE_URL}/noticias/conheca-o-novo-modelo-da-identidade-digital-padrao-do-governo-federal/edit
    Wait Until Page Contains Element  id=form.widgets.text_ifr
    Select frame  id=form.widgets.text_ifr

    # Coloca um texto único para facilitar a manipulação da âncora.
    Input text  id=content  ANCORA
    Double Click Element  xpath=//body[@id='content']/p[1]

    # O botão de link está fora do iframe de texto, então preciso sair dele.
    Unselect Frame

    Click Link  css=span .mce_link

    # Preciso agora acessar outro iframe, o do popup de edição de link.
    Wait Until Page Contains Element  id=mce_inlinepopups_31_ifr
    Select frame  id=mce_inlinepopups_31_ifr

    Click Element  css=a[href$="/noticias"]
    # Seleciona o objeto resolveuid/137b3b7b33bc4108a387d6fe475aabb8
    Click Element  css=input[href$="/noticias/titulo-da-noticia-entre-35-e-90-caracteres-com-espaco"]

    Select From List By Value  css=select#pageanchor  testeancora
    Click Button  Ok

    # Preciso sair do frame do popup para selecionar o botão do conteúdo
    Unselect Frame
    Click Button  Salvar
    Page Should Contain Element  css=a.internal-link[href$="/noticias/titulo-da-noticia-entre-35-e-90-caracteres-com-espaco#testeancora"]

Test Tinymce Ancora (Link Externo)

    Como o usuario administrador  Machado de Assis
    Ir para  ${PLONE_URL}/noticias/conheca-o-novo-modelo-da-identidade-digital-padrao-do-governo-federal/edit
    Wait Until Page Contains Element  id=form.widgets.text_ifr
    Select frame  id=form.widgets.text_ifr

    # Coloca um texto único para facilitar a manipulação da âncora.
    Input text  id=content  ANCORA
    Double Click Element  xpath=//body[@id='content']/p[1]

    # O botão de âncora está fora do iframe de texto, então preciso sair dele.
    Unselect Frame

    Click Link  css=span .mce_link

    # Preciso agora acessar outro iframe, o do popup de edição de link.
    Wait Until Page Contains Element  id=mce_inlinepopups_31_ifr
    Select frame  id=mce_inlinepopups_31_ifr

    Click Element  css=div#external_link
    Input text  id=externalurl  /noticias/titulo-da-noticia-entre-35-e-90-caracteres-com-espaco#portal-description
    Click Button  Ok

    # Preciso sair do frame do popup para selecionar o botão do conteúdo
    Unselect Frame
    Click Button  Salvar
    Page Should Contain Element  css=a.external-link[href$="/noticias/titulo-da-noticia-entre-35-e-90-caracteres-com-espaco#portal-description"]

    # Testa novamente pra verificar se o fato de salvar o objeto, não perde a
    # âncora que foi adicionada no popup via portal_transforms.
    Ir para  ${PLONE_URL}/noticias/conheca-o-novo-modelo-da-identidade-digital-padrao-do-governo-federal/edit
    Click Button  Salvar
    Page Should Contain Element  css=a.external-link[href$="/noticias/titulo-da-noticia-entre-35-e-90-caracteres-com-espaco#portal-description"]
