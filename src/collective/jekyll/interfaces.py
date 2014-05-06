from zope.interface import Interface

from zope.schema import TextLine
from zope.schema import List
from zope.schema import Int
from zope.schema import Text
from zope.schema import Object
from zope.schema import Choice

from collective.jekyll import jekyllMessageFactory as _


class ISymptom(Interface):

    title = TextLine(title=u'Title')
    help = Text(title=u'Help')
    description = Text(title=u'Description')
    status = Int(title=u'Status')

    def _update():
        pass

    def isActive():
        pass


class IDiagnosis(Interface):

    status = Int(title=u'Status')
    symptoms = List(title=u'Symptoms', value_type=Object(ISymptom))


class IIgnoredSymptomNames(Interface):
    def ignore(name):
        """store on context that symptom will be ignored"""

    def restore(name):
        """store on context that symptom will not be ignored"""

    def isIgnored(name):
        """check if symptom name is among ignored names"""


class IJekyllSettings(Interface):
    activeSymptoms = List(
        title=_(u"Active Symptoms"),
        description=_(
            u"Select which symptoms will be taken in account "
            u"when diagnosing content quality."
        ),
        required=False,
        missing_value=list(),
        value_type=Choice(
            vocabulary="collective.jekyll.SymptomsVocabulary")
    )
