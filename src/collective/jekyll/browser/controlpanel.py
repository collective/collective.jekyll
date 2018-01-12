# -*- coding: utf-8 -*-
from collective.jekyll import jekyllMessageFactory as _
from collective.jekyll.interfaces import IJekyllSettings
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout


class JekyllControlPanelForm(RegistryEditForm):
    schema = IJekyllSettings
    label = _("Content quality")
    description = _("You can activate / deactivate symptoms using this form.")


JekyllControlPanel = layout.wrap_form(
    JekyllControlPanelForm, ControlPanelFormWrapper)
