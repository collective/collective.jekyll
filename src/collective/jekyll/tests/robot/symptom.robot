*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging

Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Test cases ***

Diagnose empty description
    [tags]  testing
    Add page with empty description
    Element Should Not Be Visible  css=.symptoms
    Click element  css=.diagnosis .menuHandle
    Element Should Be Visible  css=.symptoms
    Element Should Contain  css=.name-collective-jekyll-symptoms-DescriptionLengthSymptom .symptomDescription  Description does not have content.

Diagnose valid description
    Add page with valid description
    Element Should Not Be Visible  css=.symptoms
    Click element  css=.diagnosis .menuHandle
    Element Should Be Visible  css=.symptoms

Diagnosis view
    Element Should Be Visible  css=#portaltab-diagnosis a
    Click element  css=#portaltab-diagnosis a
    Element Should Be Visible  css=#plone-contentmenu-display dt a
    Click element  css=#plone-contentmenu-display dt a
    Element Should Be Visible  css=#plone-contentmenu-display-diagnosis_view span
    Click element  css=#plone-contentmenu-display-diagnosis_view span
    Page should contain  View changed
    Element Should contain  css=.listing tr:nth-child(1) td span.globalstatus  warning
    Click link  3
    Element Should contain  css=.listing tr:nth-child(1) td span.globalstatus  ok

*** Keywords ***
Suite Setup
    Open test browser
    Enable autologin as  Manager

Add page with empty description
    Add document  Diagnose empty description
    Page should contain  warning

Add page with valid description
    Add document  Diagnose valid description
    Page should contain  warning
    Element should be visible  css=li#contentview-edit a
    Click Link  css=li#contentview-edit a
    Element Should Be Visible  css=input#title
    Input text  description  Valid description
    Click button  Save
    Page should contain  Valid description
    Page should contain  ok
