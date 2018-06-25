import unittest


class CountWords(unittest.TestCase):

    def test_no_words(self):
        from collective.jekyll.symptoms import countWords

        self.assertEquals(0, countWords(u"in the end"))

    def test_one_word(self):
        from collective.jekyll.symptoms import countWords

        self.assertEquals(1, countWords(u"in the wild"))

    def test_two_words(self):
        from collective.jekyll.symptoms import countWords

        self.assertEquals(2, countWords(u"into the wild"))
