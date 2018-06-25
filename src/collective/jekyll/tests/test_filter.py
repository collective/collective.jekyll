import unittest

from zope.component import testing
from zope.component import provideSubscriptionAdapter
from zope.component import provideAdapter


class Counter(object):

    def __init__(self):
        self.clear()

    def clear(self):
        self.value = 0

    def inc(self):
        self.value += 1

    def __str__(self):
        return repr(self.value)

counter = Counter()


def getValues(seq):
    return [value for value, diagnosis in seq]


def getStatuses(item):
    value, diag = item
    substatuses = [symptom.status for symptom in diag.symptoms]
    return value, diag.status, substatuses


class Filter(unittest.TestCase):

    def setUp(self):
        from collective.jekyll.interfaces import IDiagnosis
        from collective.jekyll.interfaces import ISymptom
        from collective.jekyll.diagnosis import Diagnosis
        from collective.jekyll.symptoms import SymptomBase

        testing.setUp(self)
        provideAdapter(Diagnosis, [int], IDiagnosis)

        class TestSymptom(SymptomBase):

            @property
            def isIgnored(self):
                return False

            @property
            def isActive(self):
                return True

        class PositiveSymptom(TestSymptom):
            title = "Positive"
            help = "Is positive."

            def _update(self):
                context = self.context
                counter.inc()
                self.status = context > 0
                if not self.status:
                    self.description = u"Is zero or negative."

        provideSubscriptionAdapter(
            PositiveSymptom, [int], ISymptom
        )

        class GreaterThanOneSymptom(TestSymptom):
            title = "Greater than one"
            help = title

            def _update(self):
                context = self.context
                self.status = context > 1
                if not self.status:
                    self.description = u"Is smaller than one."

        provideSubscriptionAdapter(
            GreaterThanOneSymptom, [int], ISymptom
        )
        counter.clear()

    def tearDown(self):
        testing.tearDown(self)

    def testCornerCases(self):
        from collective.jekyll.browser.filter import DiagnosisFilter

        values = [1, 2, 3, 4, 5, -1, -2, -3, -4, -5]

        filter = DiagnosisFilter(values, 10)
        self.assertEquals(getValues([filter[-3]]), [3])
        filter = DiagnosisFilter(values, 10)
        self.assertRaises(IndexError, filter.__getitem__, -13)
        filter = DiagnosisFilter(values, 10)
        self.assertRaises(IndexError, filter.__getitem__, 13)

    def testTrueFirst(self):
        from collective.jekyll.browser.filter import DiagnosisFilter

        values = [1, 2, 3, 4, 5, -1, -2, -3, -4, -5]

        filter = DiagnosisFilter(values, 10)

        self.assertEquals(getStatuses(filter[0]), (1, False, [True, False]))
        self.assertEquals(counter.value, 1)

        self.assertEquals(getValues(filter[:4]), [1, -1, -2, -3])
        self.assertEquals(counter.value, 8)

        self.assertEquals(getValues(filter[4:7]), [-4, -5, 2])
        self.assertEquals(counter.value, 10)

        self.assertEquals(getStatuses(filter[5]), (-5, False, [False, False]))
        self.assertEquals(counter.value, 10)

        self.assertEquals(getValues(filter[-3:]), [3, 4, 5])
        self.assertEquals(counter.value, 10)

        self.assertEquals(getStatuses(filter[9]), (5, True, [True, True]))
        self.assertEquals(getStatuses(filter[-1]), (5, True, [True, True]))

    def testFalseFirst(self):
        from collective.jekyll.browser.filter import DiagnosisFilter

        values = [-1, -2, -3, -4, -5, 1, 2, 3, 4, 5]

        filter = DiagnosisFilter(values, 10)

        self.assertEquals(getStatuses(filter[0]), (-1, False, [False, False]))
        self.assertEquals(counter.value, 1)

        self.assertEquals(getValues(filter[:4]), [-1, -2, -3, -4])
        self.assertEquals(counter.value, 4)

        self.assertEquals(getValues(filter[4:7]), [-5, 1, 2])
        self.assertEquals(counter.value, 10)

        self.assertEquals(getStatuses(filter[5]), (1, False, [True, False]))
        self.assertEquals(counter.value, 10)

        self.assertEquals(getValues(filter[-3:]), [3, 4, 5])
        self.assertEquals(counter.value, 10)

        self.assertEquals(getStatuses(filter[9]), (5, True, [True, True]))

    def testMixed(self):
        from collective.jekyll.browser.filter import DiagnosisFilter

        values = [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5]

        filter = DiagnosisFilter(values, 10)

        self.assertEquals(getStatuses(filter[0]), (-1, False, [False, False]))
        self.assertEquals(counter.value, 1)

        self.assertEquals(getValues(filter[:4]), [-1, 1, -2, -3])
        self.assertEquals(counter.value, 5)

        self.assertEquals(getValues(filter[4:7]), [-4, -5, 2])
        self.assertEquals(counter.value, 10)

        self.assertEquals(getStatuses(filter[5]), (-5, False, [False, False]))
        self.assertEquals(counter.value, 10)

        self.assertEquals(getValues(filter[-3:]), [3, 4, 5])
        self.assertEquals(counter.value, 10)

        self.assertEquals(getStatuses(filter[9]), (5, True, [True, True]))
