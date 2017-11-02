*** Settings ***

Resource  plone/app/robotframework/keywords.robot
Variables  plone/app/testing/interfaces.py
Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Variables ***

@{upload_overlay_selector}  css=form.fileupload
@{valid_types} =  image.jpg
@{invalid_types} =  file.mp3  file.ogg

*** Test cases ***

Test Upload Valid Types
    [Documentation]  Uploading image files is allowed by default

    Enable Autologin as  Site Administrator
    Goto Homepage

    Add Files  @{valid_types}
    Start Upload

    # we just assume the file was successfully upload

Test Upload Invalid Types
    [Documentation]  Uploading audio files is not allowed by default

    Enable Autologin as  Site Administrator
    Goto Homepage

    Add Files  @{invalid_types}

    # FIXME: Firefox text enconding seems to be wrong
    #        and displays "nÃ£o" instead of "não"
    #        we need to check on the ff_profile directory
    #        using this workaround meanwhile

    # an error message "File type not allowed" must be shown
    # Page Should Contain  Tipo de arquivo não permitido
    Page Should Contain Element  css=.error

*** Keywords ***

Click Add Multiple Files
    Open Add New Menu
    Click Link  css=a#multiple-files
    Wait Until Page Contains Element  @{upload_overlay_selector}

Add Files
    [Arguments]  @{files}

    Click Add Multiple Files

    # need to slow down Selenium here to avoid errors on images
    ${speed} =  Set Selenium Speed  2 seconds

    : FOR  ${file}  IN  @{files}
    \  Choose File  css=input[type=file]  /tmp/${file}
    \  Sleep  1s  Wait for file to load
    \  Page Should Contain Element  css=input[type=text][value="${file}"]

    Set Selenium Speed  ${speed}

Start Upload
    Click Button  css=.fileupload-buttonbar .start
    Wait Until Page Does Not Contain Element  @{upload_overlay_selector}
