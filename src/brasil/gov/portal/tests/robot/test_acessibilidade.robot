*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/annotate.robot
Resource  brasil/gov/portal/tests/robot/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Abrir navegador
Test Teardown  Fechar todos os navegadores


*** Test Cases ***

Contraste
    Go to  ${PLONE_URL}
	Clicar link  Contraste
	Capturar tela  contraste-ativado.png
	Clicar link  Contraste
	Capturar tela  contraste-desativado.png	

Accesskeys
	Go to  ${PLONE_URL}
	Capturar tela  accesskeys-base.png
	Clicar link  Ir para o conteúdo
	Capturar tela  accesskeys-02-conteudo.png
	Clicar link  Ir para a navegação
	Capturar tela  accesskeys-06-navegacao.png
	Clicar link  Ir para o rodapé 
	Capturar tela  accesskeys-09-rodape.png
	Clicar link  Ir para a Busca
	Pagina deve conter  Resultado da busca
	Capturar tela  accesskeys-06-busca.png

Link de acessibilidade
    Go to  ${PLONE_URL}
	Clicar link  Acessibilidade
	Capturar tela  acessibilidade-base.png
	Pagina deve conter  Tamanho do texto
	Clicar link  Grande
	Capturar tela  acessibilidade-grande.png
	Clicar link  Pequeno
	Capturar tela  acessibilidade-pequeno.png
	Clicar link  Normal
	Capturar tela  acessibilidade-normal.png