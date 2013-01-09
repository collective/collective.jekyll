import doctest
from unittest import TestSuite

from Products.PloneTestCase.PloneTestCase import setupPloneSite
from Testing.ZopeTestCase import FunctionalDocFileSuite

from plone.app.controlpanel.tests.cptc import ControlPanelTestCase

from collective.jekyll.testing import COLLECTIVE_JEKYLL_FUNCTIONAL

setupPloneSite()

OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)


class JekyllControlPanelTestCase(ControlPanelTestCase):

    layer = COLLECTIVE_JEKYLL_FUNCTIONAL


def test_suite():
    suite = TestSuite()

    suite.addTest(FunctionalDocFileSuite(
        'functional.txt',
        optionflags=OPTIONFLAGS,
        package="collective.jekyll.tests",
        test_class=JekyllControlPanelTestCase))

    return suite
