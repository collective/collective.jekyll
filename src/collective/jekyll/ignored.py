# -*- coding: utf-8 -*-
from collective.jekyll.interfaces import IIgnoredSymptomNames
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations
from zope.interface import implements
from zope.component import ComponentLookupError


JEKYLL_IGNORED_SYMPTOMS = 'JEKYLL_IGNORED_SYMPTOMS'


class IgnoredNames(object):
    implements(IIgnoredSymptomNames)

    def __init__(self, context):
        self.context = context

    def _getNamesDict(self):
        try:
           annotations = IAnnotations(self.context)
        except ComponentLookupError:
            return {}
        return annotations.setdefault(
            JEKYLL_IGNORED_SYMPTOMS, PersistentDict())

    def isIgnored(self, name):
        ignoredDict = self._getNamesDict()
        return name in ignoredDict

    def ignore(self, name):
        ignoredDict = self._getNamesDict()
        ignoredDict[name] = True

    def restore(self, name):
        ignoredDict = self._getNamesDict()
        if name in ignoredDict:
            del ignoredDict[name]
