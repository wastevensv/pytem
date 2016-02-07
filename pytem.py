#!/bin/env python3
from __future__ import print_function
import re
import markdown
from sys import argv
from util import *

try:
    input = raw_input
except NameError:
    pass


class Pytem:
    templates = {}
    global_tags = {}

    def __init__(self, templatedir, globalfile=None):
        self.templates = self._init_templates(templatedir)
        if globalfile is not None:
            try:
                with open(globalfile) as g:
                    self.global_tags = self.parse_string(g.read())
            except FileNotFoundError as e:
                print_err("ERROR: Global tag file not found.")

    def _init_templates(self, templatedir):
        templates = {"default": "%content%"}
        for fn in os.listdir(templatedir):
            if fn.endswith('.html'):  # Check for .html file extension
                fpath = os.path.join(templatedir, fn)
                with open(fpath, 'r') as f:  # Read template
                    data = f.read()
                basename = os.path.splitext(fn)[0]  # Remove file extension
                templates[basename] = data  # Associate template with name
        return templates

    def parse_string(self, data):
        tags = {}
        for line in data.split('\n'):  # Read file line by line
            p = line.split(':')  # Pairs are written as tag : value (1 per line)
            if len(p) != 2:  # If the line has any more than two parts, its not a valid pair.
                continue
            (tag, value) = (p[0], p[1])
            tag = tag.strip()  # remove whitespace from tags and values
            value = value.strip()
            tags[tag] = value  # place pair in dictionary
        return tags

    def render_string(self, text, html=False):
        parts = text.split('---')
        if len(parts) == 1:
            content = text
            data = ""
        elif len(parts) == 2:
            data = parts[0]
            content = parts[1]
        else:
            data = parts[0]
            content = "---".join(parts[1:])

        local_tags = self.parse_string(data)
        tags = self.global_tags.copy()
        tags.update(local_tags)
        if html:
            tags['content'] = content
        else:
            tags['content'] = markdown.markdown(content)

        if 'template' in tags:
            if tags['template'] in self.templates:
                template = self.templates[tags['template']]
            else:
                raise Exception("Template "+tags['template']+" not found.")
        else:
            template = self.templates['default']

        return self.render_content(template, tags)

    def render_content(self, template, tags):
        output = re.sub('%content%',tags['content'], template)
        backtick = re.compile(r'%(.*?)%')  # regex to find all tags between a pair of backticks
        for match in backtick.finditer(output):  # find all tags in the template
            tag = match.group(1)
            try:  # replace tag with value
                output = re.sub('%(' + tag + ')%', tags[tag], output)
            except:  # default to blank value
                output = re.sub('%(' + tag + ')%', "", output)
        return output

    def render_site(self, indir, outdir):
        """
        :param indir:
        :param outdir:
        :return:
        """
        delete_tree(outdir)
        create_tree(indir, outdir)  # Recreate directory tree of indir under outdir

        # iterate through all subdirectories under root.
        for root, subdirs, filenames in os.walk(indir):
            for fn in filenames:
                if fn.endswith(".html") or fn.endswith(".md"):
                    filepath = os.path.join(root,fn)
                    try:
                        with open(filepath, 'r') as f:
                            output = self.render_string(f.read(),fn.endswith(".html"))
                    except Exception as e:
                        print_err("ERROR:",e,"on",fn)
                        exit(-2)

                    # --- write content to output file ---
                    outname = os.path.splitext(fn)[0] + ".html"  # Replace .md with .html
                    subdir = get_subdir(root)
                    outpath = os.path.join(outdir, subdir, outname)
                    print_err(filepath + " -> " + outpath)
                    with open(outpath, 'w') as o:
                        o.write(output)

if __name__ == "__main__":
    if len(argv) < 4:  # print usage instructions if any parameters are missing.
        print("Usage: %s <templatedir> <indir> <outdir> (globalfile)" % argv[0])
        exit(-1)
    elif len(argv) == 4:
        Pytem(argv[1]).render_site(argv[2], argv[3])
    elif len(argv) >= 4:
        Pytem(argv[1], argv[4]).render_site(argv[2], argv[3])
