# -*- coding: utf-8 -*-
import os
import glob
import logging
import datetime
import icalendar
import urllib
from cStringIO import StringIO
from pyquery import PyQuery as pq

import webhelpers.feedgenerator as feedgenerator
from pylons import response, tmpl_context as c, url
from pylons.controllers.util import redirect

from afpyrosite.lib.base import BaseController, render

log = logging.getLogger(__name__)

docs = os.path.abspath(__file__).split('/afpyrosite/')[0]
docs = os.path.join(docs, 'docs', '_build', 'html')

meetups = (
    'http://www.meetup.com/Django-Paris/events/ical/Django+Paris/',
  )


def meetups_extends(items):
    for u in meetups:
        page = urllib.urlopen(u)
        cal = icalendar.Calendar.from_ical(page.read())
        events = [a for a in cal.walk()
                    if a.name == 'VEVENT' and 'STATUS' in a]
        for e in events:
            dt = e['DTSTART'].dt
            pubdate = datetime.datetime(dt.year, dt.month, dt.day)
            items.append((pubdate, dict(
                          title=unicode(e.get('SUMMARY')),
                          link=e['URL'],
                          pubdate=pubdate,
                          description=unicode(e['DESCRIPTION']))))


class DocsController(BaseController):

    def index(self):
        now = datetime.datetime.now()
        now = datetime.datetime(now.year, now.month, now.day)
        dates = glob.glob(os.path.join(docs, 'dates', '*', '*.html'))
        dates = [(f.split('/')[-1], f) for f in dates]
        dates = [(d.replace('.html', ''), f) for d, f in dates]
        dates = [([int(i) for i in d.split('_')], f) for d, f in dates]
        dates = [(datetime.datetime(*d), f) for d, f in dates]
        dates = sorted([(d, f) for d, f in dates if d >= now])

        if len(dates) == 1:
            doc = dates[0][1]
            doc = max(glob.glob(os.path.join(docs, 'dates', '*', '*.html')))
            doc = doc.replace('.html', '')
            year, id = doc.split('/')[-2:]
            return redirect(url('date', year=year, id=id))
        else:
            if dates:
                c.head_title = '%s AFPyros a venir!!!' % len(dates)
                c.body = ''
                for d, f in dates:
                    doc = pq(open(f).read())
                    title = doc('h1:first').html()
                    doc = f.replace('.html', '')
                    year, id = doc.split('/')[-2:]
                    c.body += '''<h2>
                    <a href="%s">%s</a>
                    </h2>''' % (
                            url('date', year=year, id=id),
                            title)

            else:
                c.head_title = 'Aucun AFPyros a venir...'
                c.body = '...'
            c.title = c.head_title
            return render('/index.html')

    def docs(self, id=None):
        doc = pq(open(os.path.join(docs, '%s.html' % id)).read())
        c.head_title = doc('h1:first').text()
        c.title = doc('h1:first').html()
        doc('h1:first').remove()
        c.body = doc('.body').html()
        return render('/index.html')

    def dates(self, year=None, id=None):
        if year and id:
            doc_path = os.path.join(docs, 'dates', year, '%s.html' % id)
            doc = pq(open(doc_path).read())
        elif id:
            doc = pq(open(os.path.join(docs, 'dates', '%s.html' % id)).read())
        doc('a.headerlink').remove()
        c.head_title = doc('h1:first').text()
        c.title = doc('h1:first').html()
        doc('h1:first').remove()
        c.body = doc('.body').html()
        return render('/index.html')

    def rss(self):
        feed = feedgenerator.Rss201rev2Feed(
                title="AFPyro",
                description="AFPyro feeds",
                link="http://afpyro.afpy.org",
                language="fr")
        items = []
        filenames = glob.glob(os.path.join(docs, '*', '*', '*.html'))
        for filename in filenames:
            doc = pq(filename=filename)
            doc('a.headerlink').remove()
            title = doc('h1:first').text()
            doc('h1:first').remove()
            body = doc('.body').html()
            path = filename.split('/dates/')[1]
            path, ext = os.path.splitext(path)
            day = path.split('/')[1]
            y, m, d = day.split('_')
            pubdate = datetime.datetime(int(y), int(m), int(d))
            items.append((pubdate, dict(
                          title=title,
                          link=u"http://afpyro.afpy.org/dates/%s.html" % path,
                          pubdate=pubdate,
                          description=body)))

        # this extend event with one found in meetup. not sure we want that
        #try:
        #    meetups_extends(items)
        #except:
        #    pass

        items = sorted(items, reverse=True)

        for d, i in items:
            feed.add_item(**i)

        response.content_type = 'application/rss+xml'
        fd = StringIO()
        feed.write(fd, 'utf-8')
        fd.seek(0)
        data = fd.read()
        return [data]
