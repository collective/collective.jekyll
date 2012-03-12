from zope.interface import Interface

from zope.schema import TextLine, Int
from zope.schema import Text



class IDiagnosis(Interface):

    title = TextLine(title=u'Title')
    description = Text(title=u'Description')
    status = Int(title=u'Status')

