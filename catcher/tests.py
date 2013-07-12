import unittest
import catcher


class CollectorTest (unittest.TestCase):
    class Tester:
        def divide(self, a, b):
            return a / b

        def inner(self):
            self.divide(2, 0)

        def test(self):
            self.inner()

    def test_collection(self):
        try:
            CollectorTest.Tester().test()
        except Exception, e:
            report = catcher.collect(e)
        html = catcher.formatters.HTMLFormatter().format(report)
        print catcher.uploaders.PasteHTMLUploader().upload(html)
        raise Exception()
        open('report.html', 'w').write(html)
