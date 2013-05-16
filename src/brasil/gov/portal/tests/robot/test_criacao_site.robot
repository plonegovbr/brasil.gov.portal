*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/annotate.robot
Resource  brasil/gov/portal/tests/robot/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Abrir navegador
Test Teardown  Fechar todos os navegadores


*** Test Cases ***

Criar novo site
    Habilitar autologin como  Manager
    Definir autologin como  Machado de Assis
    Ir para  ${ZOPE_LOGGED_URL}/@@plone-addsite?site_id=Plone
    Capturar tela  criarsite-01-base.png
    Pagina deve conter  Criar um novo site
    Campo de texto  title  Portal Brasil
    Campo de texto  orgao  Presidencia da Republica
    Campo de texto  description  Portal do Governo Brasileiro
    Capturar tela  criarsite-02-preenchido.png
    Clicar botao  Criar site Plone
    Pagina deve conter  Portal Brasil
    Pagina deve conter  Presidencia da Republica
    Pagina deve conter elemento  portal-logo
    Capturar tela  criarsite-03-sitecriado.png
    Listar rede social  youtube
    Listar rede social  twitter
    Pagina deve exibir Em Destaque

