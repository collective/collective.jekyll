import re

from bs4 import BeautifulSoup

from zope.interface import implements
from zope.i18nmessageid import Message
from zope.component import queryUtility
from zope.component import getGlobalSiteManager
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from plone.registry.interfaces import IRegistry

from collective.jekyll.interfaces import ISymptom
from collective.jekyll.interfaces import IIgnoredSymptomNames
from collective.jekyll.interfaces import IJekyllSettings
from collective.jekyll import jekyllMessageFactory as _


class Status(object):
    @property
    def status_class(self):
        return u"ok" if self.status else u"warning"

    @property
    def status_title(self):
        return _(self.status_class)


class SymptomBase(Status):
    implements(ISymptom)

    def __init__(self, context):
        self.context = context
        self.status = True
        self.description = ''
        self._registry = queryUtility(IRegistry, default={})
        self._update()

    def _update(self):
        raise NotImplementedError(u"")

    @property
    def isActive(self):
        if hasattr(self._registry, 'forInterface'):
            settings = self._registry.forInterface(IJekyllSettings, False)
            return self.name in settings.activeSymptoms
        else:
            return True

    @property
    def isIgnored(self):
        ignored = IIgnoredSymptomNames(self.context)
        return ignored.isIgnored(self.name)

    @property
    def ignored_class(self):
        return u"ignored" if self.isIgnored else u""

    @property
    def name(self):
        klass = self.__class__
        name = '.'.join((klass.__module__, klass.__name__))
        return name

    @property
    def serialized_name(self):
        return self.name.replace('.', '-')


class SymptomsVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        items = []
        gsm = getGlobalSiteManager()
        for registration in gsm.registeredSubscriptionAdapters():
            if registration.provided is ISymptom:
                symptomClass = registration.factory
                name = '.'.join((symptomClass.__module__,
                                 symptomClass.__name__))
                items.append(SimpleTerm(name,
                                        title=symptomClass.title))
        return SimpleVocabulary(items)

SymptomsVocabulary = SymptomsVocabulary()


class IdFormatSymptom(SymptomBase):

    title = _(u"Id format")
    help = (_(u"Id should not start with 'copy_of'."))

    def _update(self):
        id = self.context.getId()
        copy = re.compile('^copy[0-9]*_of')
        match = copy.match(id)
        self.status = not bool(match)
        if match:
            symptom_description = _(u"Id starts with '${start}'.")
            self.description = Message(
                symptom_description,
                mapping={'start': match.group()}
            )


class TitleLengthSymptom(SymptomBase):

    title = _(u"Title length")
    help = _(u"Title should not count too many significant words.")

    def _update(self):
        maximum = int(self._registry.get('%s.maximum' % self.name, 5))
        title = self.context.Title()
        word_count = countWords(title)
        self.status = word_count <= maximum
        symptom_description = _(
            u"The title counts ${word_count} significant words "
            u"(longer than 3 letters). "
            u"It should have at most ${maximum} significant words.")
        self.description = Message(
            symptom_description,
            mapping={'word_count': word_count, 'maximum': maximum}
        )


def countWords(string):
    words = [word for word in string.split() if len(word) > 3]
    return len(words)


class TitleFormatSymptom(SymptomBase):

    title = _(u"Title format")
    help = _(u"Title should begin with uppercase letter.")

    def _update(self):
        title = self.context.Title()
        if len(title):
            self.status = title[0].isupper()
        self.description = _(u"Title does not begin with uppercase letter.")


class DescriptionFormatSymptom(SymptomBase):

    title = _(u"Description format")
    help = _(u"Description should begin with uppercase letter.")

    def _update(self):
        description = self.context.Description()
        if len(description):
            self.status = description[0].isupper()
            self.description = _(
                u"Description does not begin with uppercase letter.")


class DescriptionLengthSymptom(SymptomBase):

    title = _(u"Description length")
    help = _(u"Description should not count too many significant words.")

    def _update(self):
        maximum = int(self._registry.get('%s.maximum' % self.name, 20))
        word_count = countWords(self.context.Description())
        if not len(self.context.Description()):
            self.status = False
            self.description = _(u"Description does not have content.")
        else:
            self.status = (word_count <= maximum)
            symptom_description = _(
                u"The description counts ${word_count} significant words "
                u"(longer than 3 letters). "
                u"It should have at most ${maximum} significant words.")
            self.description = Message(
                symptom_description,
                mapping={'word_count': word_count, 'maximum': maximum}
            )


class BodyTextPresentSymptom(SymptomBase):

    title = _(u"Body text")
    help = _(u"Body text should have content.")

    def _update(self):
        self.status = len(self.context.CookedBody(stx_level=2).strip())
        if not self.status:
            self.description = _(u"Body text does not have content.")


class SpacesInBodySymptom(SymptomBase):

    title = _(u"Spaces In Body")
    help = _(u"Body text should not start or end with empty tags or BR.")

    def _update(self):
        self.status = True
        cooked = self.context.CookedBody(stx_level=2).strip()
        soup = BeautifulSoup(cooked)
        child_count = 0
        for child in soup.children:
            child_count += 1
            if not child.previousSibling and empty_or_spaces(child.text):
                self.status = False
                self.description = _(
                    u"Body text starts with empty tags or BR.")
        if child_count != 0 and empty_or_spaces(child.text):
            self.status = False
            if child.previousSibling:
                self.description = _(u"Body text ends with empty tags or BR.")


def empty_or_spaces(text):
    #get rid of non breaking spaces
    text = text.replace(u'\xa0', u' ').strip()
    return not bool(text)


class LinksInBodySymptom(SymptomBase):

    title = _(u"Links In Body")
    help = _(u"Body text should have links.")

    def _update(self):
        self.minimum = int(self._registry.get('%s.minimum' % self.name, 2))
        cooked = self.context.CookedBody(stx_level=2).strip()
        soup = BeautifulSoup(cooked)
        links = soup.find_all('a')
        self.status = len(links) > self.minimum
        if not self.status:
            self.description = _(u"Body text does not have enough links.")


class ImagePresentSymptom(SymptomBase):

    title = _(u"Image present")
    help = _(u"Image field should have content.")

    def _update(self):
        self.status = hasImage(self.context)
        if self.status:
            self.description = _(u"Image field has content.")
        else:
            self.description = _(u"Image field does not have content.")


class ImageSizeSymptom(SymptomBase):

    title = _(u"Image size")
    help = _(u"Image field should have correct size.")

    def _update(self):
        context = self.context
        width = int(self._registry.get('%s.width' % self.name, 675))
        height = int(self._registry.get('%s.height' % self.name, 380))

        if hasImage(context):
            imageField = context.Schema()['image']
            size = imageField.getSize(context)
            self.status = size == (width, height)
        else:
            self.status = False
            size = (0, 0)
        if self.status:
            self.description = _(u"Image field content has correct size.")
        else:
            symptom_description = _(
                u"Wrong size : image is "
                u"${actual_width} by ${actual_height} pixels. "
                u"It should be ${width} by ${height} pixels."
            )
            self.description = Message(
                symptom_description,
                mapping={
                    'actual_width': size[0],
                    'actual_height': size[1],
                    'width': width,
                    'height': height
                }
            )


def hasImage(value):
    imageField = value.Schema()['image']
    status = imageField.get_size(value)
    return status
