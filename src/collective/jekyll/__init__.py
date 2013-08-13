from zope.i18nmessageid import MessageFactory
jekyllMessageFactory = MessageFactory('collective.jekyll')

DIAGNOSE_PERMISSION = 'collective.jekyll: Diagnose'
IGNORE_PERMISSION = 'collective.jekyll: Ignore'


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
