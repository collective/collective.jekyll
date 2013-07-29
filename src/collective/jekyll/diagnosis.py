from zope.interface import implements
from zope.component import subscribers

from collective.jekyll.interfaces import IDiagnosis
from collective.jekyll.interfaces import ISymptom
from collective.jekyll.symptoms import Status


class Diagnosis(Status):
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
        self._symptoms = [
            symptom
            for symptom in subscribers((self.context,), ISymptom)
            if symptom.isActive
        ]
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
        return self._mapping.get(title, None)

    def getSymptomsByStatus(self, status):
        return [symptom for symptom in self.symptoms
                if bool(symptom.status) == status]

    def sorted_symptoms(self):
        result = self.getSymptomsByStatus(False)
        result.extend(self.getSymptomsByStatus(True))
        return result


def diagnosisFromBrain(brain):
    return Diagnosis(brain.getObject())
