import doctest
from unittest import TestSuite

from plone.app.controlpanel.tests.cptc import ControlPanelTestCase

from collective.jekyll.testing import COLLECTIVE_JEKYLL_FUNCTIONAL
from plone.testing import layered


class JekyllControlPanelTestCase(ControlPanelTestCase):

    layer = COLLECTIVE_JEKYLL_FUNCTIONAL


def test_suite():
    suite = TestSuite()

    OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'functional.txt',
                optionflags=OPTIONFLAGS,
            ),
            layer=COLLECTIVE_JEKYLL_FUNCTIONAL
        ),
    ])
    return suite
