from afpyrosite.tests import *

class TestHgController(TestController):

    def test_index(self):
        resp = self.app.get(url('code', path_info='/'))
        resp.mustcontain('file')
