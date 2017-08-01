import logging, os
os.environ["HGENCODING"] = "utf-8"

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from mercurial.hgweb.hgweb_mod import hgweb
from afpyrosite.lib.base import BaseController, render
from pyquery import PyQuery as pq
from webob import Request

log = logging.getLogger(__name__)

repo = os.path.abspath(__file__).split('/afpyrosite/')[0]
app = hgweb(repo)

class HgController(BaseController):

    def index(self):
        resp = request.get_response(app)
        body = resp.body
        body = body.replace('xmlns', 'xx')
        doc = pq(body)
        c.head_title = c.title = doc('title').text() or ''
        doc('title').remove()
        c.body = doc('body').html() or ''
        c.body += doc('head').html() or ''
        request.path_info = request.script_name
        request.script_name = ''
        return render('/index.html')

