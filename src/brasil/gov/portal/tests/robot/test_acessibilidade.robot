*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/annotate.robot
Resource  brasil/gov/portal/tests/robot/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Abrir navegador
Test Teardown  Fechar todos os navegadores


*** Test Cases ***

Contraste
    Ir para  ${PLONE_URL}
	Clicar link  Contraste
	Capturar tela  contraste-ativado.png

	Clicar link  Contraste
	Capturar tela  contraste-desativado.png

Accesskeys
	Ir para  ${PLONE_URL}
	Capturar tela visivel  accesskeys-base.png

	Clicar link  Ir para o conteúdo
	Capturar tela visivel  accesskeys-02-conteudo.png

	Clicar link  Ir para a navegação
	Capturar tela visivel  accesskeys-06-navegacao.png

	Clicar link  Ir para o rodapé 
	Capturar tela visivel  accesskeys-09-rodape.png

	Clicar link  Ir para a Busca
	Pagina deve conter  Resultado da busca
	Capturar tela  accesskeys-06-busca.png

Link de acessibilidade
    Ir para  ${PLONE_URL}
	Clicar link  Acessibilidade
	Pagina deve conter  Tamanho do texto
	Capturar tela  acessibilidade-base.png

	Clicar link  Grande
	Capturar tela  acessibilidade-grande.png

	Clicar link  Pequeno
	Capturar tela  acessibilidade-pequeno.png

	Clicar link  Normal
	Capturar tela  acessibilidade-normal.png
