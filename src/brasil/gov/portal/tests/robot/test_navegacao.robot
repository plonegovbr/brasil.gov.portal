*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/annotate.robot
Resource  brasil/gov/portal/tests/robot/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Abrir navegador
Test Teardown  Fechar todos os navegadores


*** Test Cases ***

Navegacao no site
    Ir para  ${PLONE_URL}
	Capturar tela  navegacao-capa.png
	Pagina deve conter  Secretaria de
	Pagina deve conter  Comunica
	Pagina deve conter  Presid
	Clicar link  Mapa do Site
	Pagina deve conter  visualizar sua descrição.
