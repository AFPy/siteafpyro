from afpyrosite.tests import *

class TestDocsController(TestController):

    def test_index(self):
        resp = self.app.get(url('docs', id='accueil'))
        resp.mustcontain('Accueil')
