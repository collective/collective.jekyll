from zope.component.interfaces import IFactory
from zope.interface import implements

from collective.jekyll.interfaces import IDiagnosis


class DiagnosisFactory(object):
    implements(IFactory)

    def __call__(self, *args, **kwargs):
        raise NotImplemented(
                'Diagnosis should be computed by inheriting classes.')

    def getInterfaces(self):
        return IDiagnosis


class Diagnosis(object):
    implements(IDiagnosis)

    def __init__(self, title, description, status):
        self.title = title
        self.description = description
        self.status = status


class TitleLength(DiagnosisFactory):
    def __call__(self, value):
        title = value.Title()
        status = wordCount(title) <= 5
        diag = Diagnosis(u'title length', u'', status)
        return diag


def wordCount(string):
    words = [word for word in string.split() if len(word) > 3]
    return len(words)
