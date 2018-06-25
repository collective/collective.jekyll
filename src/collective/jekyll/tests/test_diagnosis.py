import unittest

from zope.component import provideSubscriptionAdapter
from zope.component import provideAdapter
import zope.component.testing

from zope.annotation.attribute import AttributeAnnotations
from zope.annotation.interfaces import IAnnotations


class ToDiagnose(object):

    def __init__(self, id='id', title='title'):
        self.id = id
        self.title = title

    def getId(self):
        return self.id

    def Title(self):
        return self.title


class TestDiagnosis(unittest.TestCase):

    def setUp(self):
        from collective.jekyll.interfaces import ISymptom
        from collective.jekyll.interfaces import IIgnoredSymptomNames
        from collective.jekyll.ignored import IgnoredNames
        from collective.jekyll.symptoms import IdFormatSymptom
        from collective.jekyll.symptoms import TitleLengthSymptom

        zope.component.testing.setUp()
        provideAdapter(AttributeAnnotations, (ToDiagnose,), IAnnotations)
        provideAdapter(IgnoredNames, (ToDiagnose,), IIgnoredSymptomNames)
        provideSubscriptionAdapter(IdFormatSymptom, (ToDiagnose,), ISymptom)
        provideSubscriptionAdapter(TitleLengthSymptom, (ToDiagnose,), ISymptom)

    def tearDown(self):
        zope.component.testing.tearDown()

    def test_diagnosis_ok(self):
        from collective.jekyll.diagnosis import Diagnosis
        context = ToDiagnose()
        diagnosis = Diagnosis(context)
        self.assertEquals(diagnosis.status, True)
        self.assertEquals(2, len(diagnosis.getSymptomsByStatus(True)))
        self.assertEquals(0, len(diagnosis.getSymptomsByStatus(False)))

    def test_diagnosis_not_ok(self):
        from collective.jekyll.diagnosis import Diagnosis
        from collective.jekyll.symptoms import IdFormatSymptom
        from collective.jekyll.symptoms import TitleLengthSymptom
        context = ToDiagnose('copy_of')
        diagnosis = Diagnosis(context)
        self.assertEquals(diagnosis.status, False)
        self.assertEquals(1, len(diagnosis.getSymptomsByStatus(True)))
        self.assertEquals(1, len(diagnosis.getSymptomsByStatus(False)))
        sorted = diagnosis.sorted_symptoms()
        self.assertTrue(isinstance(sorted[0], IdFormatSymptom))
        self.assertTrue(isinstance(sorted[1], TitleLengthSymptom))

    def test_diagnosis_ok_because_ignored(self):
        from collective.jekyll.diagnosis import Diagnosis
        from collective.jekyll.symptoms import IdFormatSymptom
        from collective.jekyll.symptoms import TitleLengthSymptom
        from collective.jekyll.interfaces import IIgnoredSymptomNames

        context = ToDiagnose('copy_of')
        diagnosis = Diagnosis(context)
        name = IdFormatSymptom(context).name
        symptom = diagnosis.getSymptomByName(name)
        self.assertEquals(diagnosis.status, False)
        self.assertEquals(symptom.isIgnored, False)
        ignored = IIgnoredSymptomNames(context)
        ignored.ignore(name)
        diagnosis = Diagnosis(context)
        symptom = diagnosis.getSymptomByName(name)
        self.assertEquals(symptom.isIgnored, True)
        self.assertEquals(diagnosis.status, True)
        self.assertEquals(1, len(diagnosis.getSymptomsByStatus(True)))
        self.assertEquals(1, len(diagnosis.getSymptomsByStatus(False)))
        sorted = diagnosis.sorted_symptoms()
        self.assertTrue(isinstance(sorted[0], TitleLengthSymptom))
        self.assertTrue(isinstance(sorted[1], IdFormatSymptom))
