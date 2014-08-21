*** Settings ***

Variables  brasil/gov/portal/tests/robot/variables.py

*** Keywords ***

# ----------------------------------------------------------------------------
# Navegador
# ----------------------------------------------------------------------------

Abrir navegador
    Open browser  ${START_URL}  ${BROWSER}
    ...           remote_url=${REMOTE_URL}
    ...           desired_capabilities=${DESIRED_CAPABILITIES}
    ...           ff_profile_dir=${FF_PROFILE}

Fechar todos os navegadores
    Close all browsers

# ----------------------------------------------------------------------------
# Traducoes
# ----------------------------------------------------------------------------

Como o usuario administrador
    [Arguments]  ${username}
    Enable autologin as  Manager
    Definir autologin como   ${username}

Habilitar autologin como 
    [Arguments]  ${role}
    Enable autologin as  ${role}

Definir autologin como 
    [Arguments]  ${username}
    Set autologin username  ${username}

Ir para 
    [Arguments]  ${url}
    Go to  ${url}

Capturar tela 
    [Arguments]  ${filename}
    Capture page screenshot  ${filename} 

Capturar tela visivel
    [Arguments]  ${filename}
    Capture page screenshot  ${filename}
    @{dimensions} =  Execute Javascript
    ...    return (function(){
    ...        var w = window, d = document, e = d.documentElement,
    ...            g = d.getElementsByTagName('body')[0], x = 0, y = 0,
    ...            width = w.innerWidth || e.clientWidth || g.clientWidth,
    ...            height = w.innerHeight || e.clientHeight || g.clientHeight;
    ...        if (typeof pageYOffset != 'undefined') { y = pageYOffset; }
    ...        else {
    ...           if (e.clientHeight) { y = e.scrollTop; /* IE 'stdsmode' */ }
    ...           else { y = d.body.scrollTop; /* IE 'quirksmode' */ }
    ...        }
    ...        return [x, y, width, height];
    ...    })();
    Crop image  ${OUTPUT_DIR}  ${filename}  @{dimensions}

Pagina deve conter 
    [Arguments]  ${text}
    Page should contain  ${text}

Pagina deve conter elemento 
    [Arguments]  ${element}
    Page should contain element  ${element}

Pagina deve exibir Em Destaque
    Page should contain element  em-destaque

Listar rede social 
    [Arguments]  ${name}
    Element Should be visible  css=div#social-icons  #portalredes-${name}

Campo de texto 
    [Arguments]  ${field}  ${value}
    Input text for sure  ${field}  ${value}

Clicar botao 
    [Arguments]  ${value}
    Click Button  ${value}

Clicar link 
    [Arguments]  ${value}
    Click Link  ${value}

Abrir o menu 
    [Arguments]  ${elementId}

    Element Should Be Visible  css=dl#${elementId} span
    Element Should Not Be Visible  css=dl#${elementId} dd.actionMenuContent
    Click link  css=dl#${elementId} dt.actionMenuHeader a
    Wait until keyword succeeds  1  5  Element Should Be Visible  css=dl#${elementId} dd.actionMenuContent

Abrir o menu de Adicionar item
    Element Should Be Visible  css=dl#plone-contentmenu-factories
    Element Should Not Be Visible  css=dl#plone-contentmenu-factories dd.actionMenuContent
    Click link  css=dl#plone-contentmenu-factories dt.actionMenuHeader a
    Wait until keyword succeeds  1  5  Element Should Be Visible  css=dl#plone-contentmenu-factories dd.actionMenuContent
