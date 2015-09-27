import os, sys
from .pytem import Pytem

subject = Pytem("template",'globalfile')


def tag_test():
    result = subject.render_string("title : Title---%title%")
    assert result == "<p>Title</p>"


def md_test():
    result = subject.render_string("---#Hello World")
    assert result == "<h1>Hello World</h1>"


def site_test():
    os.environ["PROMPT"] = "no"
    return subject.render_site("in","out")
