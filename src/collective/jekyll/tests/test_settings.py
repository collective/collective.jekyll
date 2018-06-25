import unittest

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from plone.registry.interfaces import IRegistry

from collective.jekyll.interfaces import IJekyllSettings
from collective.jekyll.testing import COLLECTIVE_JEKYLL_INTEGRATION

SYMPTOMS_ACTIVE_BY_PROFILE = [
    'collective.jekyll.symptoms.IdFormatSymptom',
    'collective.jekyll.symptoms.TitleLengthSymptom',
    'collective.jekyll.symptoms.DescriptionLengthSymptom']


class TestSettings(unittest.TestCase):

    layer = COLLECTIVE_JEKYLL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

    def testRegistryAfterSetup(self):
        """
        """
        settings = getUtility(
            IRegistry, context=self.portal).forInterface(
                IJekyllSettings, False)
        self.assertIsNotNone(settings.activeSymptoms)
        self.assertEquals(
            len(settings.activeSymptoms), len(SYMPTOMS_ACTIVE_BY_PROFILE))
        for symptom in SYMPTOMS_ACTIVE_BY_PROFILE:
            self.assertTrue(symptom in settings.activeSymptoms)

    def testVocabulary(self):
        vocabFactory = getUtility(
            IVocabularyFactory, name="collective.jekyll.SymptomsVocabulary")
        symptoms = vocabFactory(self.portal)
        values = [symptom.value for symptom in symptoms]
        for symptom in SYMPTOMS_ACTIVE_BY_PROFILE:
            self.assertTrue(symptom in values)
