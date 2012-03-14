from zope.component.interfaces import IFactory
from zope.interface import implements

from collective.jekyll.interfaces import ISymptom


class SymptomFactory(object):
    implements(IFactory)

    def __init__(self, context):
        self.context = context

    def __call__(self, *args, **kwargs):
        raise NotImplemented(
                'Symptom should be computed by inheriting classes.')

    def getInterfaces(self):
        return ISymptom


class Symptom(object):
    implements(ISymptom)

    def __init__(self, title, help, status, description):
        self.title = title
        self.help = help
        self.status = status
        self.description = description


class TitleLengthFactory(SymptomFactory):

    title = u"Title length"
    help = (u"Title should not count more than 5 significant words "
            u"(of more than three letters).")

    def __call__(self):
        title = self.context.Title()
        word_count = countWords(title)
        status = word_count <= 5
        description = u"The title counts %d words" % word_count
        symptom = Symptom(self.title, self.help, status, description)
        return symptom


def countWords(string):
    words = [word for word in string.split() if len(word) > 3]
    return len(words)


class DescriptionLengthFactory(SymptomFactory):

    title = u"Description length"
    help = (u"Description should not count more than 20 significant words "
            u"(of more than three letters).")

    def __call__(self):
        word_count = countWords(self.context.Description())
        status = word_count <= 20
        description = u"The description counts %d words" % word_count
        symptom = Symptom(self.title, self.help, status, description)
        return symptom


class BodyTextPresentFactory(SymptomFactory):

    title = u"Body text present"
    help = u"Body text has content."

    def __call__(self):
        status = len(self.context.CookedBody(stx_level=2).strip())
        if status:
            description = self.help
        else:
            description = u"Body text has no content."
        symptom = Symptom(self.title, self.help, status, description)
        return symptom


class ImagePresentFactory(SymptomFactory):

    title = u"Image present"
    help = u"Image field has content."

    def __call__(self):
        status = hasImage(self.context)
        if status:
            description = self.help
        else:
            description = u"Image field has no content."
        symptom = Symptom(self.title, self.help, status, description)
        return symptom


class ImageSizeFactory(SymptomFactory):

    title = u"Image size"
    help = u"Image field has correct size."

    def __call__(self):
        context = self.context
        if hasImage(context):
            imageField = context.Schema()['image']
            size = imageField.getSize(context)
            status = size == (675, 380)
        else:
            status = False
            size = (0, 0)
        if status:
            description = self.help
        else:
            description = (u"Image field has wrong size : %d, %d" %
                    (size[0], size[1]))
        symptom = Symptom(self.title, self.help, status, description)
        return symptom


def hasImage(value):
    imageField = value.Schema()['image']
    status = imageField.get_size(value)
    return status
