from __future__ import print_function
import os, shutil, sys

__author__ = 'William'


def print_err(*args):
    print(*args, file=sys.stderr)


def get_subdir(dirs):
    subdirs = dirs.split(os.sep)[1:]  # return subdirectory path exclduing the root directory
    return os.sep.join(subdirs)


def delete_tree(dst):  # Create directory tree from src in dst
    for name in os.listdir(dst):
            if name == ".git":
                continue
            if os.path.isdir(os.path.join(dst, name)):
                print_err("Deleting %s" % os.path.join(dst,name))
                delete_tree(os.path.join(dst, name))
                os.rmdir(os.path.join(dst, name))
                continue
            print_err("Deleting %s" % os.path.join(dst,name))
            os.remove(os.path.join(dst, name))

def create_tree(src, dst):
    copy_files(src, dst)
    print_err("Creating directories in %s"%dst)
    for name in os.listdir(src):
        print_err("Copying %s" % os.path.join(src, name))
        if os.path.isdir(os.path.join(src, name)):
                print_err("Copying Directory %s" % os.path.join(src, name))
                os.mkdir(os.path.join(dst, name))
                create_tree(os.path.join(src, name), os.path.join(dst, name))

def copy_files(src, dst):
    print_err("Creating files in %s"%dst)
    for name in os.listdir(src):
        if not os.path.isdir(os.path.join(src, name)) and not name.endswith('.md'):
            print_err("Copying File %s" % os.path.join(src, name), os.path.join(dst, name))
            shutil.copy(os.path.join(src, name), os.path.join(dst, name))

def md_files_only(src, names):
    ignore = [n for n in names if n.endswith('.md')]
    return ignore


def files_only(src, names):
    if src.endswith("res"):  # Copy files from resource folders
        return []
    else:  # Otherwise, only copy directories.
        return [name for name in names if
                not os.path.isdir(os.path.join(src, name))]  # return only the directories in src
