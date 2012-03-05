from zope.interface import Interface

from zope.schema import TextLine
from zope.schema import Text


class ISymptom(Interface):

    title = TextLine(u'Title')

    def __call__(value):
        """returns True if symptom is not present, False otherwise"""
