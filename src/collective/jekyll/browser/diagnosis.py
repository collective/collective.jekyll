from Products.Five import BrowserView

from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.PloneBatch import Batch

from collective.jekyll.browser.filter import DiagnosisFilter
from collective.jekyll.interfaces import IDiagnosis


class DiagnosisItem(BrowserView):

    @property
    def diagnosis(self):
        return IDiagnosis(self.context)


class DiagnosisCollectionView(BrowserView):

    def items(self):
        b_start = int(self.request.get('b_start', 0))
        b_size = 20
        context = self.context
        pcatalog = getToolByName(context, 'portal_catalog')
        query = context.buildQuery()
        results = pcatalog.searchResults(query)
        total_length = len(results)
        filter = DiagnosisFilter(results, total_length)
        results = Batch(filter, b_size, b_start)
        return results
