import re

from bs4 import BeautifulSoup

from zope.interface import implements
from zope.component import getUtility

from plone.registry.interfaces import IRegistry

from collective.jekyll.interfaces import ISymptom
from collective.jekyll.interfaces import IIsActive


class SymptomBase(object):
    implements(ISymptom)

    def __init__(self, context):
        self.context = context
        self.status = True
        self.description = ''
        self._update()

    def _update(self):
        raise NotImplemented(
                'Update should be computed by inheriting classes.')

    @property
    def isActive(self):
        return IIsActive(self).isActive


class ActiveSymptom(object):
    implements(IIsActive)

    def __init__(self, context):
        self.context = context

    @property
    def isActive(self):
        registry = getUtility(IRegistry)
        active = registry.get(self.name, True)
        return active

    @property
    def name(self):
        klass = self.context.__class__
        return '.'.join((klass.__module__, klass.__name__))


class IdFormatSymptom(SymptomBase):

    title = u"Id format"
    help = (u"Id should not start with 'copy_of'.")

    def _update(self):
        id = self.context.getId()
        copy = re.compile('^copy[0-9]*_of')
        match = copy.match(id)
        self.status = not bool(match)
        if match:
            self.description = u"Id starts with '%s'." % match.group()


class TitleLengthSymptom(SymptomBase):

    title = u"Title length"
    help = (u"Title should not count more than 5 significant words "
            u"(of more than three letters).")

    def _update(self):
        title = self.context.Title()
        word_count = countWords(title)
        self.status = word_count <= 5
        self.description = u"The title counts %d words" % word_count


def countWords(string):
    words = [word for word in string.split() if len(word) > 3]
    return len(words)


class TitleFormatSymptom(SymptomBase):

    title = u"Title format"
    help = (u"Title should begin with uppercase letter.")

    def _update(self):
        title = self.context.Title()
        if len(title):
            self.status = title[0].isupper()
        self.description = u"Title does not begin with uppercase letter."


class DescriptionFormatSymptom(SymptomBase):

    title = u"Description format"
    help = (u"Description should begin with uppercase letter.")

    def _update(self):
        description = self.context.Description()
        if len(description):
            self.status = description[0].isupper()
            self.description = (u"Description does not begin "
                    u"with uppercase letter.")


class DescriptionLengthSymptom(SymptomBase):

    title = u"Description length"
    help = (u"Description should not count more than 20 significant words "
            u"(of more than three letters).")

    def _update(self):
        word_count = countWords(self.context.Description())
        self.status = (word_count <= 20) and (word_count > 0)
        self.description = u"The description counts %d words" % word_count


class BodyTextPresentSymptom(SymptomBase):

    title = u"Body text"
    help = u"Body text should have content."

    def _update(self):
        self.status = len(self.context.CookedBody(stx_level=2).strip())
        if not self.status:
            self.description = u"Body text has no content."


class SpacesInBodySymptom(SymptomBase):

    title = u"Spaces In Body"
    help = u"Body text should not start or end with empty tags or BR."

    def _update(self):
        self.status = True
        cooked = self.context.CookedBody(stx_level=2).strip()
        soup = BeautifulSoup(cooked)
        child_count = 0
        for child in soup.children:
            child_count += 1
            if not child.previousSibling and empty_or_spaces(child.text):
                self.status = False
                self.description = u"Body text starts with empty tags or BR."
        if child_count != 0 and empty_or_spaces(child.text):
            self.status = False
            if child.previousSibling:
                self.description = u"Body text ends with empty tags or BR."


def empty_or_spaces(text):
    #get rid of non breaking spaces
    text = text.replace(u'\xa0', u' ').strip()
    return not bool(text)


class LinksInBodySymptom(SymptomBase):

    title = u"Links In Body"
    help = u"Body text should have 2 links."

    def _update(self):
        cooked = self.context.CookedBody(stx_level=2).strip()
        soup = BeautifulSoup(cooked)
        links = soup.find_all('a')
        self.status = len(links) > 1
        if not self.status:
            self.description = u"Body text has no links."


class ImagePresentSymptom(SymptomBase):

    title = u"Image present"
    help = u"Image field should have content."

    def _update(self):
        self.status = hasImage(self.context)
        if self.status:
            self.description = u"Image field has content."
        else:
            self.description = u"Image field has no content."


class ImageSizeSymptom(SymptomBase):

    title = u"Image size"
    help = u"Image field should have correct size."

    def _update(self):
        context = self.context
        if hasImage(context):
            imageField = context.Schema()['image']
            size = imageField.getSize(context)
            self.status = size == (675, 380)
        else:
            self.status = False
            size = (0, 0)
        if self.status:
            self.description = u"Image field content has correct size."
        else:
            self.description = (
                u"Image field content has wrong size : %d, %d" %
                (size[0], size[1]))


def hasImage(value):
    imageField = value.Schema()['image']
    status = imageField.get_size(value)
    return status
