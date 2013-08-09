from Products.Five import BrowserView

from Products.CMFPlone.PloneBatch import Batch

from plone.app.layout.viewlets.common import ViewletBase

from plone.memoize import view

from collective.jekyll.browser.filter import DiagnosisFilter
from collective.jekyll.interfaces import IDiagnosis
from collective.jekyll.interfaces import IIgnoredSymptomNames


class DiagnosisViewlet(ViewletBase):

    @property
    def diagnosis(self):
        return IDiagnosis(self.context)


class DiagnosisCollectionView(BrowserView):

    @view.memoize
    def items(self):
        b_start = int(self.request.get('b_start', 0))
        b_size = 20
        context = self.context
        results = context.getQuery(brains=True)
        total_length = len(results)
        filter = DiagnosisFilter(results, total_length)
        results = Batch(filter, b_size, b_start)
        return results

    @view.memoize
    def getSymptomTypes(self):
        helps = []
        for item, diagnosis in self.items():
            for symptom in diagnosis.symptoms:
                help = dict(title=symptom.title, help=symptom.help)
                if help not in helps:
                    helps.append(help)
        return helps


class IgnoreSymptomView(BrowserView):

    def __call__(self):
        name = self.request.symptomName
        ignored = IIgnoredSymptomNames(self.context)
        ignored.ignore(name)
        self.request.RESPONSE.redirect(self.context.absolute_url())


class RestoreSymptomView(BrowserView):

    def __call__(self):
        name = self.request.symptomName
        ignored = IIgnoredSymptomNames(self.context)
        ignored.restore(name)
        self.request.RESPONSE.redirect(self.context.absolute_url())
