__author__ = 'William'
from sys import argv
from .pytem import Pytem

if __name__ == "__main__":
    if len(argv) < 4:  # print usage instructions if any parameters are missing.
        print("Usage: %s <templatedir> <indir> <outdir> (globalfile)" % argv[0])
        exit(-1)
    elif len(argv) == 4:
        Pytem(argv[1]).render_site(argv[2], argv[3])
    elif len(argv) >= 4:
        Pytem(argv[1], argv[4]).render_site(argv[2], argv[3])
