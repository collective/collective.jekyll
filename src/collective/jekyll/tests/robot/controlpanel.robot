*** Settings ***
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  plone.app.robotframework.keywords.Debugging

Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Test cases ***

Viewing the jekyll control panel
    [tags]  testing
    Go to  ${PLONE_URL}/@@jekyll-controlpanel
    Location should contain  jekyll-controlpanel
    Click button  Save
    Wait until page contains  Changes saved.
    Location should contain  jekyll-controlpanel

Deactivating all symptoms, then activating just 2
    [tags]  testing
    Go to  ${PLONE_URL}/@@jekyll-controlpanel
    Select all from list  name=form.widgets.activeSymptoms.to
    Click button  name=to2fromButton
    Click button  Save
    Wait until page contains  Changes saved.
    ${to}=  Get List Items  name=form.widgets.activeSymptoms.to
    Should Be Empty  ${to}
    Select from list  name=form.widgets.activeSymptoms.from  Short Name format
    Click button  name=from2toButton
    Select from list  name=form.widgets.activeSymptoms.from  Title length
    Click button  name=from2toButton
    Click button  Save
    Wait until page contains  Changes saved.
    ${to}=  Get List Items  name=form.widgets.activeSymptoms.to
    ${expected}=  Create List  Short Name format  Title length
    Should be equal  ${to}  ${expected}

*** Keywords ***
Suite Setup
    Open test browser
    Enable autologin as  Manager
