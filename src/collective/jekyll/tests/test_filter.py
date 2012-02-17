import unittest2 as unittest


class Counter(object):

    def __init__(self, value):
        self.value = value

    def clear(self):
        self.value = 0

    def inc(self):
        self.value += 1

    def __str__(self):
        return repr(self.value)


def getValues(seq):
    return [value for value, whole, items in seq]


class Filter(unittest.TestCase):

    counter = Counter(0)

    def tearDown(self):
        self.counter.clear()

    def isPositive(self, value):
        self.counter.inc()
        return value > 0

    def isGreatherThanOne(self, value):
        return value > 1

    def testTrueFirst(self):
        from collective.jekyll.browser.filter import DiagnosisFilter

        values = [1, 2, 3, 4, 5, -1, -2, -3, -4, -5]

        filter = DiagnosisFilter(
                [self.isPositive, self.isGreatherThanOne], values, 10)

        self.assertEquals(filter[0], (1, False, [True, False]))
        self.assertEquals(self.counter.value, 1)

        self.assertEquals(getValues(filter[:4]), [1, -1, -2, -3])
        self.assertEquals(self.counter.value, 8)

        self.assertEquals(getValues(filter[4:7]), [-4, -5, 2])
        self.assertEquals(self.counter.value, 10)

        self.assertEquals(filter[5], (-5, False, [False, False]))
        self.assertEquals(self.counter.value, 10)

        self.assertEquals(getValues(filter[-3:]), [3, 4, 5])
        self.assertEquals(self.counter.value, 10)

        self.assertEquals(filter[9], (5, True, [True, True]))

    def testFalseFirst(self):
        from collective.jekyll.browser.filter import DiagnosisFilter

        values = [-1, -2, -3, -4, -5, 1, 2, 3, 4, 5]

        filter = DiagnosisFilter(
                [self.isPositive, self.isGreatherThanOne], values, 10)

        self.assertEquals(filter[0], (-1, False, [False, False]))
        self.assertEquals(self.counter.value, 1)

        self.assertEquals(getValues(filter[:4]), [-1, -2, -3, -4])
        self.assertEquals(self.counter.value, 4)

        self.assertEquals(getValues(filter[4:7]), [-5, 1, 2])
        self.assertEquals(self.counter.value, 10)

        self.assertEquals(filter[5], (1, False, [True, False]))
        self.assertEquals(self.counter.value, 10)

        self.assertEquals(getValues(filter[-3:]), [3, 4, 5])
        self.assertEquals(self.counter.value, 10)

        self.assertEquals(filter[9], (5, True, [True, True]))

    def testMixed(self):
        from collective.jekyll.browser.filter import DiagnosisFilter

        values = [-1, 1, -2, 2, -3, 3, -4, 4, -5, 5]

        filter = DiagnosisFilter(
                [self.isPositive, self.isGreatherThanOne], values, 10)

        self.assertEquals(filter[0], (-1, False, [False, False]))
        self.assertEquals(self.counter.value, 1)

        self.assertEquals(getValues(filter[:4]), [-1, 1, -2, -3])
        self.assertEquals(self.counter.value, 5)

        self.assertEquals(getValues(filter[4:7]), [-4, -5, 2])
        self.assertEquals(self.counter.value, 10)

        self.assertEquals(filter[5], (-5, False, [False, False]))
        self.assertEquals(self.counter.value, 10)

        self.assertEquals(getValues(filter[-3:]), [3, 4, 5])
        self.assertEquals(self.counter.value, 10)

        self.assertEquals(filter[9], (5, True, [True, True]))
