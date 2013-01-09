from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility
from zope.formlib import form
from zope.schema.interfaces import IVocabularyFactory

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.registry.interfaces import IRegistry
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.widgets import MultiCheckBoxThreeColumnWidget

from collective.jekyll import jekyllMessageFactory as _
from collective.jekyll.interfaces import IJekyllSettings


class JekyllControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IJekyllSettings)

    def __init__(self, context):
        super(JekyllControlPanelAdapter, self).__init__(context)
        self.settings = getUtility(IRegistry).forInterface(IJekyllSettings, False)
        vocabFactory = getUtility(IVocabularyFactory,
                                  name="collective.jekyll.SymptomsVocabulary")
        self.symptoms = vocabFactory(context)


    def getActiveSymptoms(self):
        if self.settings.activeSymptoms is None:
            return [s.value for s in self.symptoms]

        activeSymptoms = []
        for symptom in self.symptoms:
            if symptom.value in self.settings.activeSymptoms:
                activeSymptoms.append(symptom.value)
        return activeSymptoms

    def setActiveSymptoms(self, value):
        self.settings.activeSymptoms = value

    activeSymptoms = property(getActiveSymptoms,
                              setActiveSymptoms)


class JekyllControlPanel(ControlPanelForm):

    label = _("Jekyll symptoms")
    description = _("You can activate / deactivate symptoms using this form.")
    form_name = _("Jekyll symptoms activation settings")

    form_fields = form.FormFields(IJekyllSettings)
    form_fields['activeSymptoms'].custom_widget = MultiCheckBoxThreeColumnWidget
    form_fields['activeSymptoms'].custom_widget.cssClass = 'label'
