*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/annotate.robot
Resource  brasil/gov/portal/tests/robot/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Abrir navegador
Test Teardown  Fechar todos os navegadores


*** Test Cases ***

Criar novo site
    Como o usuario administrador  Machado de Assis
    Ir para  ${NOVO_SITE_URL}
    Capturar tela  criarsite-passo-01.png

    Pagina deve conter elemento  title_1
    Campo de texto  title_1  Portal do
    Campo de texto  title_2  Governo Eletronico
    Campo de texto  orgao  Ministerio do Planejamento
    Campo de texto  description  Portal do Governo Brasileiro
    Capturar tela  criarsite-passo-02.png
    Clicar botao  Criar Portal

    Pagina deve conter  Portal do
    Pagina deve conter  Governo Eletronico
    Pagina deve conter  Ministerio do Planejamento
    Pagina deve conter elemento  portal-logo
    Listar rede social  youtube
    Listar rede social  twitter
    Pagina deve exibir Em Destaque
    Capturar tela  criarsite-passo-03.png

Conteudo base - Pasta de Imagens
    Como o usuario administrador  Machado de Assis
    Ir para  ${PLONE_URL}/imagens
    Capturar tela  criarsite-passo-04-pasta-imagens.png

Conteudo base - Pasta Assuntos
    Como o usuario administrador  Machado de Assis
    Ir para  ${PLONE_URL}/assuntos
    Capturar tela  criarsite-passo-04-pasta-assuntos.png

Conteudo base - Pasta Acesso a Informacao
    Como o usuario administrador  Machado de Assis
    Ir para  ${PLONE_URL}/acesso-a-informacao
    Capturar tela  criarsite-passo-05-pasta-acesso-a-informacao.png

Alterar dados do site
    Como o usuario administrador  Machado de Assis
    Ir para  ${PLONE_URL}/@@site-controlpanel
    Campo de texto  form.site_title_1  Secretaria de
    Campo de texto  form.site_title_2  Comunicacao Social
    Campo de texto  form.site_orgao  Presidencia da Republica
    Campo de texto  form.site_description  Site da SECOM
    Clicar botao  Salvar

    Ir para  ${PLONE_URL}
    Pagina deve conter  Secretaria de
    Pagina deve conter  Comunicacao Social


Validar se Portal Padrao esta listado
    Como o usuario administrador  Machado de Assis
    Ir para  ${PLONE_URL}/prefs_install_products_form
    Capturar tela  criarsite-passo-06-validar-produto-portal-padrao.png
