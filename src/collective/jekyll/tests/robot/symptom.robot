*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Test cases ***

Diagnose empty description
    Add document  Diagnose empty description
    Page should contain  warning
    Element Should Not Be Visible  css=.symptoms
    Click element  css=.diagnosis .menuHandle
    Element Should Be Visible  css=.symptoms
    Element Should Contain  css=.symptoms  The description counts 0 words

Diagnose valid description
    Add document  Diagnose valid description
    Page should contain  warning
    Element should be visible  css=li#contentview-edit a
    Click Link  css=li#contentview-edit a
    Element Should Be Visible  css=input#title
    Input text  description  Valid description
    Click button  Save
    Page should contain  Valid description
    Page should contain  ok
    Element Should Not Be Visible  css=.symptoms
    Click element  css=.diagnosis .menuHandle
    Element Should Be Visible  css=.symptoms

*** Keywords ***
Suite Setup
    Open test browser
    Enable autologin as  Manager
