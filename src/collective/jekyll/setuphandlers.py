def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile(
        'collective_jekyll_various.txt') is None:
        return
    portal = context.getSite()
    folder_id = portal.invokeFactory('Folder', 'pages')
    folder = getattr(portal, folder_id)
    for i in range(40):
        make_subfolder(folder, str(i + 1))
    topic_id = portal.invokeFactory('Collection', 'diagnosis', title="Diagnosis")
    topic = getattr(portal, topic_id)
    topic.setQuery([{'portal_type': 'Document'}])


def make_subfolder(folder, index):
    subfolder_id = folder.invokeFactory('Folder', 'subfolder_%s' % index)
    subfolder = getattr(folder, subfolder_id)
    subfolder.invokeFactory('Document', 'ok', title="Ok page")
    subfolder.invokeFactory('Document', 'error', title="Error")
