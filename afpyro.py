import datetime
import glob
import os
import io
from types import SimpleNamespace

import feedgenerator
from flask import (
    Flask,
    escape,
    request,
    render_template,
    redirect,
    url_for,
    Markup,
    Response,
)
from pyquery import PyQuery as pq

app = Flask(__name__)
docs = os.path.dirname(os.path.abspath(__file__))
docs = os.path.join(docs, "docs", "_build", "html")


@app.route("/")
def index():
    now = datetime.datetime.now()
    now = datetime.datetime(now.year, now.month, now.day)
    dates = glob.glob(os.path.join(docs, "dates", "*", "*.html"))
    dates = [(f.split("/")[-1], f) for f in dates]
    dates = [(d.replace(".html", ""), f) for d, f in dates]
    dates = [([int(i) for i in d.split("_")], f) for d, f in dates]
    dates = [(datetime.datetime(*d), f) for d, f in dates]
    dates = sorted([(d, f) for d, f in dates if d >= now])
    c = SimpleNamespace()
    if len(dates) == 1:
        doc = dates[0][1]
        doc = max(glob.glob(os.path.join(docs, "dates", "*", "*.html")))
        doc = doc.replace(".html", "")
        year, id = doc.split("/")[-2:]
        return redirect(url_for("date", year=year, id=id))
    else:
        if dates:
            c.head_title = f"{len(date)} AFPyros a venir!!!" % len(dates)
            c.body = ""
            for d, f in dates:
                doc = pq(open(f).read())
                doc.remove_namespaces()
                title = doc("h1:first").html()
                doc = f.replace(".html", "")
                year, id = doc.split("/")[-2:]
                c.body += """<h2>
                <a href="%s">%s</a>
                </h2>""" % (
                    url("date", year=year, id=id),
                    title,
                )

        else:
            c.head_title = "Aucun AFPyros a venir..."
            c.body = "..."
        c.title = c.head_title
        return render_template("index.html", c=c)


def from_sphinx(name):
    c = SimpleNamespace()
    doc = pq(open(os.path.join(docs, f"{name}.html")).read())
    doc.remove_namespaces()
    c.head_title = doc("h1:first").text()
    c.title = Markup(doc("h1:first").html())
    doc("h1:first").remove()
    c.body = Markup(doc(".body").html())
    return render_template("index.html", c=c)


@app.route("/accueil.html")
def accueil():
    return from_sphinx("accueil")


@app.route("/dates.html")
def dates():
    return from_sphinx("dates")


@app.route("/faq.html")
def faq():
    return from_sphinx("faq")


@app.route("/contribute.html")
def contribute():
    return from_sphinx("contribute")


@app.route("/dates/<id>.html")
@app.route("/dates/<year>/<id>.html")
def dates_detail(year=None, id=None):
    c = SimpleNamespace()
    if year and id:
        doc_path = os.path.join(docs, "dates", year, "%s.html" % id)
        doc = pq(open(doc_path).read())
    elif id:
        doc = pq(open(os.path.join(docs, "dates", "%s.html" % id)).read())
    doc.remove_namespaces()
    doc("a.headerlink").remove()
    c.head_title = doc("h1:first").text()
    c.title = Markup(doc("h1:first").html())
    doc("h1:first").remove()
    c.body = Markup(doc(".body").html())
    return render_template("index.html", c=c)


@app.route("/afpyro.rss")
def rss():
    feed = feedgenerator.Rss201rev2Feed(
        title="AFPyro",
        description="AFPyro feeds",
        link="http://afpyro.afpy.org",
        language="fr",
    )
    items = []
    filenames = glob.glob(os.path.join(docs, "*", "*", "*.html"))
    for filename in filenames:
        doc = pq(filename=filename)
        doc("a.headerlink").remove()
        title = doc("h1:first").text()
        doc("h1:first").remove()
        body = doc(".body").html()
        path = filename.split("/dates/")[1]
        path, ext = os.path.splitext(path)
        day = path.split("/")[1]
        y, m, d = day.split("_")
        pubdate = datetime.datetime(int(y), int(m), int(d))
        items.append(
            (
                pubdate,
                dict(
                    title=title,
                    link="http://afpyro.afpy.org/dates/%s.html" % path,
                    pubdate=pubdate,
                    description=body,
                ),
            )
        )

    items = sorted(items, reverse=True)

    for d, i in items:
        feed.add_item(**i)

    fd = io.StringIO()
    feed.write(fd, "utf-8")
    fd.seek(0)
    data = fd.read()
    return Response(data, content_type="application/rss+xml")
