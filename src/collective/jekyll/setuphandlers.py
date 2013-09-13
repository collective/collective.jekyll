from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from plone.registry.interfaces import IRegistry

from collective.jekyll.interfaces import IJekyllSettings


def setupSettings(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile(
            'collective_jekyll_various.txt') is None:
        return
    portal = context.getSite()
    settings = getUtility(IRegistry).forInterface(IJekyllSettings, False)
    if settings.activeSymptoms is None:
        vocabFactory = getUtility(IVocabularyFactory,
                                  name="collective.jekyll.SymptomsVocabulary")
        symptoms = vocabFactory(portal)
        settings.activeSymptoms = [s.value for s in symptoms]


def testSetup(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile(
            'collective_jekyll_test.txt') is None:
        return
    portal = context.getSite()
    if 'pages' not in portal.objectIds():
        folder_id = portal.invokeFactory('Folder', 'pages')
        folder = getattr(portal, folder_id)
        for i in range(40):
            make_subfolder(folder, str(i + 1))
    if 'diagnosis' not in portal.objectIds():
        topic_id = portal.invokeFactory(
            'Collection', 'diagnosis', title="Diagnosis")
        topic = getattr(portal, topic_id)
        topic.setQuery([
            {'i': 'portal_type',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': ['Document']}])


def make_subfolder(folder, index):
    subfolder_id = folder.invokeFactory('Folder', 'subfolder_%s' % index)
    subfolder = getattr(folder, subfolder_id)
    subfolder.setTitle(subfolder_id)
    subfolder.invokeFactory(
        'Document', 'ok', title="Ok page", description="Description")
    subfolder.invokeFactory('Document', 'error', title="Error")
