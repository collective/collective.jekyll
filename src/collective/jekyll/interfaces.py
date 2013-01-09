from zope.interface import Interface

from zope.schema import TextLine
from zope.schema import List
from zope.schema import Bool
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


class IIsActive(Interface):

    isActive = Bool(title=u'isActive')
    name = TextLine(title=u'Name')


class IDiagnosis(Interface):

    status = Int(title=u'Status')
    symptoms = List(title=u'Symptoms', value_type=Object(ISymptom))


class IJekyllSettings(Interface):
    activeSymptoms = List(
        title=_(u"Active Symptoms"),
        description=_(u"You can define which symptoms will be active to "
                      u"diagnose your content by checking / unchecking them."),
        required=False,
        missing_value=list(),
        value_type=Choice(
            vocabulary="collective.jekyll.SymptomsVocabulary")
        )
