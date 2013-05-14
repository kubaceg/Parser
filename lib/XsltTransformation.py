__author__ = 'kuba'

import sys, os, getopt, shlex
from subprocess import Popen, PIPE, STDOUT



class XsltTransformation:
    xsltFile = "wsdl2rdf_v3.xsl"
    inputfile = ''
    outputfile = ''

    def xsltTransformation(self):
        fileList = os.listdir(self.inputfile)
        counter = 0
        total = len(fileList)
        print "Transforming wsdl\'s..."
        for file in fileList:
            sys.stdout.write('\t' + str(counter) + ' of ' + str(total) + ' files transformed\r')
            filename = os.path.splitext(os.path.basename(file))[0]
            out = Popen(shlex.split('xsltproc --stringparam filename "' + filename + '"' + " " + self.xsltFile + " " + self.inputfile+file), stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()[0]
            file = open(self.outputfile+'/'+filename+".rdf", 'w')
            file.write(out)
            file.close()
            counter += 1
        sys.stdout.write('\t' + str(counter) + ' of ' + str(total) + ' files transformed')

    def __init__(self, inputfile, outputfile):
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.xsltTransformation()