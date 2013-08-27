from plone.testing import z2
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

import collective.jekyll


COLLECTIVE_JEKYLL = PloneWithPackageLayer(
    zcml_package=collective.jekyll,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.jekyll:testing',
    name='COLLECTIVE_JEKYLL'
)

COLLECTIVE_JEKYLL_INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_JEKYLL, ),
    name="COLLECTIVE_JEKYLL_INTEGRATION"
)

COLLECTIVE_JEKYLL_FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_JEKYLL, ),
    name="COLLECTIVE_JEKYLL_FUNCTIONAL"
)

COLLECTIVE_JEKYLL_ZSERVER = FunctionalTesting(
    bases=(COLLECTIVE_JEKYLL, z2.ZSERVER_FIXTURE),
    name="COLLECTIVE_JEKYLL_ZSERVER"
)

COLLECTIVE_JEKYLL_ROBOT_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_JEKYLL, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="COLLECTIVE_JEKYLL_ROBOT_TESTING")
