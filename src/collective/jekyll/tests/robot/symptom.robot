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
    Diagnosis should be warning
    Diagnosis menu should be closed
    Click to open diagnosis menu
    Symptom IdFormatSymptom should be ok
    IdFormatSymptom should not be ignored
    Symptom TitleLengthSymptom should be ok
    TitleLengthSymptom should not be ignored
    Symptom DescriptionLengthSymptom should be warning
    Description of symptom DescriptionLengthSymptom should be Description does not have content.
    DescriptionLengthSymptom should not be ignored
    DescriptionLengthSymptom should have Ignore link

Ignore empty description
    [tags]  testing
    Add page with empty description
    Click to open diagnosis menu
    Click DescriptionLengthSymptom Ignore link
    Diagnosis should be ok
    Diagnosis menu should be closed
    Click to open diagnosis menu
    DescriptionLengthSymptom should be ignored
    DescriptionLengthSymptom should have Consider link
    Click DescriptionLengthSymptom Consider link
    Diagnosis should be warning
    Diagnosis menu should be closed
    Click to open diagnosis menu
    DescriptionLengthSymptom should not be ignored
    DescriptionLengthSymptom should have Ignore link

Diagnose valid description
    Add page with valid description
    Diagnosis should be ok
    Diagnosis menu should be closed
    Click to open diagnosis menu
    Symptom IdFormatSymptom should be ok
    IdFormatSymptom should not be ignored
    Symptom TitleLengthSymptom should be ok
    TitleLengthSymptom should not be ignored
    Symptom DescriptionLengthSymptom should be ok
    DescriptionLengthSymptom should not be ignored

Diagnosis view
    Element Should Be Visible  css=#portaltab-diagnosis a
    Click element  css=#portaltab-diagnosis a
    Element Should Be Visible  css=#plone-contentmenu-display dt a
    Click element  css=#plone-contentmenu-display dt a
    Element Should Be Visible  css=#plone-contentmenu-display-diagnosis_view span
    Click element  css=#plone-contentmenu-display-diagnosis_view span
    Page should contain  View changed
    Page should contain  [1]
    Element Should contain  css=.listing tr:nth-child(1) td span.globalstatus  warning
    Click link  3
    Page should contain  [3]
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

Diagnosis should be ${status}
    Page should contain element  css=dt.diag-${status}.globalstatus
    
Diagnosis menu should be closed
    Element Should Not Be Visible  css=.symptoms

Diagnosis menu should be opened
    Element Should Be Visible  css=.symptoms

Click to open diagnosis menu
    Diagnosis menu should be closed
    Page should contain element  css=.diagnosis .menuHandle
    Click element  css=.diagnosis .menuHandle
    Diagnosis menu should be opened

Symptom ${symptom_class} should be ${symptom_status}
    ${status_selector} =  set variable  css=.name-collective-jekyll-symptoms-${symptom_class} .diag-${symptom_status}
    Page should contain element  ${status_selector} 
    Element should be visible  ${status_selector}
    Element should contain  ${status_selector}  ${symptom_status}

Description of symptom ${symptom_class} should be ${symptom_description}
    ${description_selector} =  set variable  css=.name-collective-jekyll-symptoms-${symptom_class} .symptomDescription
    Page Should Contain Element  ${description_selector}
    Element Should Be Visible  ${description_selector}
    Element Should Contain  ${description_selector}  ${symptom_description}

${symptom_class} should have ${link_text} link
    ${link_selector} =  set variable  css=.name-collective-jekyll-symptoms-${symptom_class} .symptomDescription a
    Page Should Contain Element  ${link_selector}
    Element Should Be Visible  ${link_selector} 
    Element Should contain  ${link_selector}  ${link_text}

Click ${symptom_class} ${link_text} link
    ${symptom_class} should have ${link_text} link
    ${link_selector} =  set variable  css=.name-collective-jekyll-symptoms-${symptom_class} .symptomDescription a
    Click Element  ${link_selector}

${symptom_class} should be ignored
    ${symptom_selector} =  set variable  css=.name-collective-jekyll-symptoms-${symptom_class}
    ${ignored_selector} =  set variable  ${symptom_selector}.ignored
    Page Should Contain Element  ${ignored_selector}
    Element Should Be Visible  ${ignored_selector} 

${symptom_class} should not be ignored
    ${symptom_selector} =  set variable  css=.name-collective-jekyll-symptoms-${symptom_class}
    ${ignored_selector} =  set variable  ${symptom_selector}.ignored
    Page Should Contain Element  ${symptom_selector}
