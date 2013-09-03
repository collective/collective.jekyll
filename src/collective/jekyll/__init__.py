from zope.i18nmessageid import MessageFactory
jekyllMessageFactory = _ = MessageFactory('collective.jekyll')

DIAGNOSE_PERMISSION = 'collective.jekyll: Diagnose'
IGNORE_PERMISSION = 'collective.jekyll: Ignore'

OK = _(u'ok')
WARNING = _(u'warning')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
