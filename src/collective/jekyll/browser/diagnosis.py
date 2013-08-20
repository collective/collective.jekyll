from AccessControl import getSecurityManager

from zope.i18n import translate

from Products.Five import BrowserView
from Products.CMFPlone.PloneBatch import Batch

from plone.app.layout.viewlets.common import ViewletBase

from plone.memoize import view

from collective.jekyll.browser.filter import DiagnosisFilter
from collective.jekyll.interfaces import IDiagnosis
from collective.jekyll.interfaces import IIgnoredSymptomNames
from collective.jekyll import jekyllMessageFactory as _
from collective.jekyll import IGNORE_PERMISSION


class DiagnosisViewlet(ViewletBase):

    @property
    def diagnosis(self):
        return IDiagnosis(self.context)


class DiagnosisCollectionView(BrowserView):

    @view.memoize
    def items(self):
        b_start = int(self.request.get('b_start', 0))
        b_size = 20
        results = self._getResults()
        total_length = len(results)
        filter = DiagnosisFilter(results, total_length)
        results = Batch(filter, b_size, b_start)
        return results

    def _getResults(self):
        return self.context.getQuery(brains=True)

    @view.memoize
    def getSymptomTypes(self):
        helps = []
        for item, diagnosis in self.items():
            for symptom in diagnosis.symptoms:
                help = dict(title=symptom.title, help=symptom.help)
                if help not in helps:
                    helps.append(help)
        return helps


class DiagnosisTopicView(DiagnosisCollectionView):
    "for old-style collection (ATTopic)"

    def _getResults(self):
        from Products.CMFCore.utils import getToolByName

        context = self.context
        pcatalog = getToolByName(context, 'portal_catalog')
        query = context.buildQuery()
        return pcatalog.searchResults(query)


class SymptomView(BrowserView):

    def ignore_action(self):
        content = self.context.context
        sm = getSecurityManager()
        if not sm.checkPermission(IGNORE_PERMISSION, content):
            return u''
        return self._make_link()

    def _make_link(self):
        content = self.context.context
        if self.context.isIgnored:
            link_text = translate(_(u"Restore"), context=self.request)
            action = u"restore"
        else:
            link_text = translate(_(u"Ignore"), context=self.request)
            action = u"ignore"
        url = u'{url}/jekyll_{action}_symptom?symptomName={name}'.format(
            url=content.absolute_url(),
            name=self.context.name,
            action=action,
        )
        return u'<a href="{url}">{text}</a>'.format(
            url=url,
            text=link_text,
        )


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
