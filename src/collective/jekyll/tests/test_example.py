import unittest

from zope.component import getMultiAdapter
from zope.event import notify
from zope.traversing.interfaces import BeforeTraverseEvent


from Products.CMFCore.utils import getToolByName

from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

from collective.jekyll.testing import COLLECTIVE_JEKYLL_INTEGRATION


class TestIntegration(unittest.TestCase):

    layer = COLLECTIVE_JEKYLL_INTEGRATION

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        notify(BeforeTraverseEvent(self.portal, self.request))

    def test_product_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        qi_tool = getToolByName(self.portal, 'portal_quickinstaller')
        pid = 'collective.jekyll'
        installed = [p['id'] for p in qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')

    def test_collection_view(self):
        diagnosis = self.portal.diagnosis
        from zope.interface import alsoProvides
        from collective.jekyll.browser.interfaces import IThemeSpecific
        alsoProvides(self.request, IThemeSpecific)
        diagnosis_view = getMultiAdapter(
            (diagnosis, self.request),
            name="diagnosis_view"
        )
        content = diagnosis_view()
        WARNING = '<span class="status diag-warning">warning</span>'
        self.assertTrue(WARNING in content)
        SYMPTOM = 'name-collective-jekyll-symptoms-DescriptionLengthSymptom'
        self.assertTrue(SYMPTOM in content)

    def test_viewlet(self):
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Editor', 'Member'])
        pages = self.portal.pages
        content = pages()
        VIEWLET = '<dl class="diagnosis menu">'
        self.assertTrue(VIEWLET in content)
