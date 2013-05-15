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