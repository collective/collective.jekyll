from plone.testing import layered

import robotsuite

from collective.jekyll.testing import COLLECTIVE_JEKYLL_ROBOT_TESTING


def test_suite():
    return layered(robotsuite.RobotTestSuite('robot/symptom.robot'),
                layer=COLLECTIVE_JEKYLL_ROBOT_TESTING)
