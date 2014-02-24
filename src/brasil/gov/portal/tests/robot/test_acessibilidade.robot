*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/annotate.robot
Resource  brasil/gov/portal/tests/robot/keywords.robot

Library  WAVELibrary
Library  Remote  ${PLONE_URL}/RobotRemote
Library  brasil.gov.portal.tests.robot.acessibilidade.Acessibilidade

Test Setup  Abrir navegador
Test Teardown  Fechar todos os navegadores


*** Test Cases ***

Alto Contraste Desativado
    Ir para  ${PLONE_URL}
	Clicar link  Alto Contraste
	Capturar tela  contraste-ativado.png
	Verificar erros de acessibilidade

Alto Contraste Ativado
	Clicar link  Alto Contraste
	Capturar tela  contraste-desativado.png
	Verificar erros de acessibilidade
 
Validar contraste de elementos
	[Template]  Validar contraste do elemento com id
	portal-title-1
	portal-title
	portal-description
	link-conteudo
	link-navegacao
	link-buscar
	link-rodape
	em-destaque-titulo
	portalservicos-contato

Validar contraste de elementos com alto contraste ativado
	[Template]  Validar contraste do elemento com id em alto contraste
	portal-title-1
	portal-title
	portal-description
	link-conteudo
	link-navegacao
	link-buscar
	link-rodape
	em-destaque-titulo
	portalservicos-contato


Accesskeys
	Ir para  ${PLONE_URL}
	Capturar tela visivel  accesskeys-base.png
	Verificar erros de acessibilidade

	Clicar link  Ir para o conteúdo
	Capturar tela visivel  accesskeys-01-conteudo.png

	Clicar link  Ir para a navegação
	Capturar tela visivel  accesskeys-02-navegacao.png

	Clicar link  Ir para a Busca
	Capturar tela  accesskeys-03-busca.png

	Clicar link  Ir para o rodapé 
	Capturar tela visivel  accesskeys-04-rodape.png

Link de acessibilidade
    Ir para  ${PLONE_URL}/acessibilidade
	Pagina deve conter  Decreto
	Pagina deve conter  5.296
	Capturar tela  acessibilidade-base.png
	Verificar erros de acessibilidade


Validar acessibilidade nas paginas
    [Template]  Verificar erros de acessibilidade na URL 
    ${PLONE_URL}/@@search
    ${PLONE_URL}/folder_contents


*** Keywords ***

Validar contraste do elemento com id 
	[Arguments]  ${element_id}
	${selector} =  Evaluate  str('#${element_id}')
	Validar contraste do elemento  ${selector}

Validar contraste do elemento  
    [Arguments]  ${selector}
    @{info} =  Execute Javascript
    ...    return (function(){
    ...     function element_info(element){
    ...     	var oElement = element;
    ...     	var eStyle = window.getComputedStyle(element);
    ...     	var bg = eStyle.color;
    ...     	var fg = eStyle.backgroundColor;
    ...         while ((fg == "rgba(0, 0, 0, 0)") || (fg == "transparent")){
    ... 			element = element.parentNode;
    ... 			fg = window.getComputedStyle(element).backgroundColor;
    ... 		}
    ...     	var size = eStyle.getPropertyValue("font-size");
    ...         element = oElement; 
    ...         while (!size){
    ... 			element = element.parentNode;
    ... 			size = window.getComputedStyle(element).getPropertyValue("font-size");
    ... 		}
    ...     	return [bg, fg, size];
    ...     }    
    ...    	var element = jQuery('${selector}');
    ...     if (element.length === 0) { return [];}
    ...    	element = element[0];   
    ...    	var _element_info = element_info(element);   
    ...    	var bg = _element_info[0];
    ...    	var fg = _element_info[1];
    ...    	var size = _element_info[2];    
    ...    	return [bg, fg, size];
    ...    })();
    Validate Contrast AA  ${selector}  @{info}

Validar contraste do elemento com id em alto contraste
    [Arguments]  ${element_id}
    Delete Cookie  contraste
    Ir para  ${PLONE_URL}
    Clicar link  Alto Contraste
	Validar contraste do elemento com id  ${element_id}

Verificar erros de acessibilidade
    Check accessibility errors

Verificar erros de acessibilidade na URL 
	[Arguments]  ${URL}
    Check URL for accessibility errors  ${URL}
