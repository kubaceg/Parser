#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys, os, getopt
import lib.XsltTransformation as XsltTransform
import lib.WordnetTriples as WordnetTriples


def getParams(argv):
    global inputfile
    global outputfile
    helpMsg = 'parser.py -i <directory with wsdl> -o <directory with output>'
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print helpMsg
        sys.exit(2)
    if len(opts) == 0:
        print helpMsg
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print helpMsg
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if not (os.path.exists(outputfile)):
        os.mkdir(outputfile)


if __name__ == "__main__":
    getParams(sys.argv[1:])
    xslt = XsltTransform(inputfile, outputfile)
