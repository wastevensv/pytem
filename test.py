from __future__ import print_function
import os, sys
from .pytem import Pytem


def print_err(*args):
    print(*args, file=sys.stderr)

subject = Pytem("template",'globalfile')


def tag_test():
    result = subject.render_string("title : Title---%title%")
    print_err(result)
    assert result == "<p>Title</p>"


def md_test():
    result = subject.render_string("---#Hello World")
    print_err(result)
    assert result == "<h1>Hello World</h1>"


def dual_delim_test():
    result = subject.render_string("title : Title---%title%---More Content")
    print_err(result)
    assert result == "<p>Title---More Content</p>"


def site_test():
    os.environ["PROMPT"] = "no"
    return subject.render_site("in","out")
