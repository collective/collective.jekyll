from Products.Five import BrowserView

from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.PloneBatch import Batch

from collective.jekyll.browser.filter import DiagnosisFilter


class Diagnosis(BrowserView):

    def items(self):
        b_start = int(self.request.get('b_start', 0))
        b_size = 7
        context = self.context
        pcatalog = getToolByName(context, 'portal_catalog')
        query = context.buildQuery()
        results = pcatalog.searchResults(query)
        total_length = len(results)
        filter = DiagnosisFilter([self.ok, self.inThree],
                results, total_length)
        results = Batch(filter, b_size, b_start)
        return results

    def getTestsTitles(self):
        return "Id is not error", "Url has no '3'"

    def ok(self, value):
        object = value.getObject()
        diag = object.getId() != 'error'
        return diag

    def inThree(self, value):
        object = value.getObject()
        diag = '3' not in object.absolute_url()
        return diag

    def error(self, value):
        return not self.ok(value)
