from zope.interface import Interface

from zope.schema import TextLine
from zope.schema import List
from zope.schema import Bool
from zope.schema import Int
from zope.schema import Text
from zope.schema import Object


class ISymptom(Interface):

    title = TextLine(title=u'Title')
    help = Text(title=u'Help')
    description = Text(title=u'Description')
    status = Int(title=u'Status')


class IDiagnosis(Interface):

    status = Int(title=u'Status')
    symptoms = List(title=u'Symptoms', value_type=Object(ISymptom))
