from Products.Five import BrowserView

from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.PloneBatch import Batch

from collective.jekyll.browser.filter import DiagnosisFilter


class Diagnosis(BrowserView):

    def items(self):
        b_start = int(self.request.get('b_start', 0))
        b_size = 20
        context = self.context
        pcatalog = getToolByName(context, 'portal_catalog')
        query = context.buildQuery()
        results = pcatalog.searchResults(query)
        total_length = len(results)
        tests = [hasBody, titleLengthOk, descriptionLengthOk, hasImage, imageSizeOk]
        filter = DiagnosisFilter(tests, results, total_length)
        results = Batch(filter, b_size, b_start)
        return results

    def getTestsTitles(self):
        return "Corps du texte rempli", "Longueur titre", "Longueur description", "Image presente", "Taille image"


def hasBody(value):
    obj = value.getObject()
    diag = len(obj.CookedBody(stx_level=2).strip())
    return diag


def titleLengthOk(value):
    obj = value.getObject()
    title = obj.Title()
    diag = wordCount(title) <= 5
    return diag


def descriptionLengthOk(value):
    obj = value.getObject()
    description = obj.Description()
    diag = wordCount(description) <= 20
    return diag


def wordCount(string):
    words = [word for word in string.split() if len(word) > 3]
    return len(words)


def hasImage(value):
    obj = value.getObject()
    imageField = obj.Schema()['image']
    diag = imageField.get_size(obj)
    return diag

    
def imageSizeOk(value):
    if hasImage(value):
        obj = value.getObject()
        imageField = obj.Schema()['image']
        diag = imageField.getSize(obj) == (675, 380)
    else:
        diag = False
    return diag
