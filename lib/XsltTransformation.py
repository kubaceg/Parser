__author__ = 'kuba'

import sys, os, getopt, subprocess


class XsltTransformation:
    xsltFile = "wsdl2rdf_v3.xsl"
    inputfile = ''
    outputfile = ''

    def getParams(self, argv):

        global inputfile
        global outputfile
        try:
            opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
        except getopt.GetoptError:
            print 'parser.py -i <directory with wsdl> -o <directory with output>'
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print 'parser.py -i <directory with wsdl> -o <directory with output>'
                sys.exit()
            elif opt in ("-i", "--ifile"):
                self.inputfile = arg
            elif opt in ("-o", "--ofile"):
                self.outputfile = arg
        os.mkdir(self.outputfile)


    def xsltTransformation(self):
        fileList = os.listdir(self.inputfile)
        counter = 0
        total = len(fileList)
        print "Transforming wsdl\'s..."
        for file in fileList:
            sys.stdout.write('\t' + str(counter) + ' of ' + str(total) + ' files transformed\r')
            subprocess.Popen(['xsltproc', '--stringparam filename "' + os.path.basename(
                file) + '" ' + self.xsltFile + " " + file + " > " + self.outputfile + "/" + os.path.basename(file)],
                             stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
            counter += 1
        sys.stdout.write('\t' + str(counter) + ' of ' + str(total) + ' files transformed')

    def __init__(self, argv):
        self.getParams(argv)
        self.xsltTransformation()