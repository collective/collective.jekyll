from zope.interface import implements
from zope.component import subscribers

from collective.jekyll.interfaces import IDiagnosis
from collective.jekyll.interfaces import ISymptomFactory


class Diagnosis(object):
    implements(IDiagnosis)

    def __init__(self, context):
        self.context = context
        self._factories = None
        self._symptoms = []
        self._status = True

    def _update(self):
        symptoms = self._symptoms 
        if not symptoms:
            for factory in self._getFactories():
                symptom = factory()
                self._status = self._status and symptom.status
                symptoms.append(symptom)

    def _getFactories(self):
        if self._factories is None:
            self._factories = subscribers((self.context,), ISymptomFactory)
        return self._factories
   
    @property
    def symptoms(self):
        self._update()
        return self._symptoms
    
    @property
    def status(self):
        self._update()
        return self._status
    
    @property
    def symptoms_help(self):
        results = []
        for name, factory in self._getFactoriesFor():
            results.append((factory.title, factory.help))
        return results
   

def diagnosisFromBrain(brain):
    return Diagnosis(brain.getObject())
