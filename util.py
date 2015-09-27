from __future__ import print_function
import os, shutil, sys

__author__ = 'William'


def print_err(*args):
    print(*args, file=sys.stderr)


def get_subdir(dirs):
    subdirs = dirs.split(os.sep)[1:]  # return subdirectory path exclduing the root directory
    return os.sep.join(subdirs)


def create_tree(src, dst):  # Create directory tree from src in dst
    try:
        shutil.copytree(src, dst, ignore=md_files_only)  # If directory doesn't exist yet, just make it.
    except OSError as e:  # If directory already exists, prompt before deleting.
        if os.environ.get('PROMPT', "yes").lower() == "no":
            shutil.rmtree(dst)
            create_tree(src, dst)
            return
        sys.stdout.write("%s exists, Overwrite (y/n) " % dst)
        overwrite = input()
        if overwrite == 'y' or overwrite == 'Y':  # If user agrees, delete and try again.
            print_err("Deleting %s" % dst)
            shutil.rmtree(dst)
            print_err("Creating directories")
            create_tree(src, dst)
        else:  # Exit with error if not overwriting.
            raise Exception("Directory exists, not overwriting, exiting.")


def md_files_only(src, names):
    ignore = [n for n in names if n.endswith('.md')]
    return ignore


def files_only(src, names):
    if src.endswith("res"):  # Copy files from resource folders
        return []
    else:  # Otherwise, only copy directories.
        return [name for name in names if
                not os.path.isdir(os.path.join(src, name))]  # return only the directories in src
