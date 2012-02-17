from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.jekyll


COLLECTIVE_JEKYLL = PloneWithPackageLayer(collective.jekyll,
'collective.jekyll:default', name='COLLECTIVE_JEKYLL')

COLLECTIVE_JEKYLL_INTEGRATION = \
    IntegrationTesting(bases=(COLLECTIVE_JEKYLL, ),
                       name="COLLECTIVE_JEKYLL_INTEGRATION")

COLLECTIVE_JEKYLL_FUNCTIONAL = \
    FunctionalTesting(bases=(COLLECTIVE_JEKYLL, ),
                       name="COLLECTIVE_JEKYLL_FUNCTIONAL")
