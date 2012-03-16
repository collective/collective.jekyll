from zope.interface import implements

from collective.jekyll.interfaces import ISymptom


class SymptomBase(object):
    implements(ISymptom)

    def __init__(self, context):
        self.context = context
        self._update()

    def _update(self):
        raise NotImplemented(
                'Update should be computed by inheriting classes.')


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
        if self.status:
            self.description = u"Body text has some content."
        else:
            self.description = u"Body text has no content."


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
