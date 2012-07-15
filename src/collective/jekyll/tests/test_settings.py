import unittest2 as unittest

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from plone.registry.interfaces import IRegistry

from collective.jekyll.interfaces import IJekyllSettings
from collective.jekyll.testing import COLLECTIVE_JEKYLL_INTEGRATION


class TestSettings(unittest.TestCase):

    layer = COLLECTIVE_JEKYLL_INTEGRATION

    def setUp(self):
        self.portal = self.layer['portal']

    def testRegistryAfterSetup(self):
        """
        """
        settings = getUtility(IRegistry,
                              context=self.portal).forInterface(IJekyllSettings,
                                                                False)
        self.assertIsNotNone(settings.activeSymptoms)
        vocabFactory = getUtility(IVocabularyFactory,
                                  name="collective.jekyll.SymptomsVocabulary")
        symptoms = vocabFactory(self.portal)
        self.assertEquals(len(settings.activeSymptoms), len(symptoms))
        for symptom in symptoms:
            self.assertTrue(symptom.value in settings.activeSymptoms)
