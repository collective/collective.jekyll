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
        self._byTitle = {}
        self._byName = {}
        self._status = True
        self._invalid = True
        self.cache = {}

    def _update(self):
        if self._invalid:
            self._updateSymptoms()
            self._updateStatus()
            self._invalid = False

    def _updateStatus(self):
        self._status = True
        for symptom in self._symptoms:
            if hasattr(symptom, 'setCache'):
                symptom.setCache(self.cache)
            symptom._update()
            if symptom not in self._ignored_symptoms:
                self._status = self._status and symptom.status

    def _updateSymptoms(self):
        self._symptoms = [
            symptom
            for symptom in subscribers((self.context,), ISymptom)
            if symptom.isActive
        ]
        for symptom in self._symptoms:
            self._byTitle[symptom.title] = symptom
            self._byName[symptom.name] = symptom
        self._ignored_symptoms = [
            symptom 
            for symptom in self._symptoms
            if symptom.isIgnored
        ]

    @property
    def symptoms(self):
        self._update()
        return self._symptoms

    @property
    def status(self):
        self._update()
        return self._status

    def getSymptomByTitle(self, title):
        self._update()
        return self._byTitle.get(title, None)

    def getSymptomByName(self, name):
        self._update()
        return self._byName.get(name, None)

    def getStatusByName(self, name):
        symptom = self.getSymptomByName(name)
        if symptom is None:
            return True
        else:
            return symptom.status

    def getSymptomsByStatus(self, status):
        return [
            symptom
            for symptom in self.symptoms
            if bool(symptom.status) == status
        ]

    def sorted_symptoms(self):
        result = self.getSymptomsByStatus(False)
        result.extend(self.getSymptomsByStatus(True))
        result = [
            symptom
            for symptom in result
            if symptom not in self.ignored_symptoms
        ]
        result.extend(self.ignored_symptoms)
        return result

    @property
    def ignored_symptoms(self):
        self._update()
        return self._ignored_symptoms


def diagnosisFromBrain(brain):
    return Diagnosis(brain.getObject())
