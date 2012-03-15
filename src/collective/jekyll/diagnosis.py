from zope.interface import implements
from zope.component import subscribers

from collective.jekyll.interfaces import IDiagnosis
from collective.jekyll.interfaces import ISymptom


class Diagnosis(object):
    implements(IDiagnosis)

    def __init__(self, context):
        self.context = context
        self._symptoms = None
        self._mapping = {}
        self._status = True

    def _update(self):
        if not self._symptoms:
            self._updateSymptoms()
            for symptom in self._symptoms:
                self._status = self._status and symptom.status

    def _updateSymptoms(self):
        self._symptoms = subscribers((self.context,), ISymptom)
        for symptom in self._symptoms:
            self._mapping[symptom.title] = symptom
   
    @property
    def symptoms(self):
        self._update()
        return self._symptoms
    
    @property
    def status(self):
        self._update()
        return self._status

    def getSymptomByTitle(self, title):
        return self._mapping[title]
    

def diagnosisFromBrain(brain):
    return Diagnosis(brain.getObject())
