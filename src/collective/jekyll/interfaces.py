from zope.interface import Interface

from zope.component.interfaces import IFactory

from zope.schema import TextLine
from zope.schema import List
from zope.schema import Int
from zope.schema import Text
from zope.schema import Tuple
from zope.schema import Object


class ISymptom(Interface):

    title = TextLine(title=u'Title')
    help = Text(title=u'Help')
    description = Text(title=u'Description')
    status = Int(title=u'Status')


class ISymptomFactory(IFactory):
    
    title = TextLine(title=u'Title')
    help = Text(title=u'Help')


class IDiagnosis(Interface):

    status = Int(title=u'Status')
    symptoms = List(title=u'Symptoms', value_type=Object(ISymptom))
    symptoms_help = List(title=u'Symptoms help',
            value_type=Tuple(value_type=Text()))

