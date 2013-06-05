__author__ = 'kuba'

from lxml import etree
import re
from nltk.corpus import wordnet as wn


class WordnetTriples:
    host = "http://127.0.0.1/"

    def extractWords(self, pureLabel):
        words = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', pureLabel).lower().split("_")
        return filter(lambda a: a != '', words) # Remove empty string from list

    def getAllLabels(self, file):
        NSMAP = {'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                                             "inf": "http://127.0.0.1/inference#"}
        document = etree.parse(file)
        results = document.xpath("//*/*/inf:hasLabel/@rdf:resource", namespaces=NSMAP) # Get all labels

        for label in results:
            synset = ''
            synset += '<inf:label rdf:about="%s">'%(label)
            pureLabel = label[label.find("(") + 1:-1]

            words = self.extractWords(pureLabel)

            for word in words:
                synset+='<inf:hasTerm rdf:resource="%sTerm(%s)"/>'%(self.host, word)
            synset += '</inf:label>'

            for word in words:
                synsets = wn.synsets(word) # get all synsets
                synset += '<inf:term rdf:about="%sTerm(%s)">'%(self.host, word)
                for syn in synsets:
                    synset+='<inf:isa rdf:resource="%s%s" />'%(self.host, syn)
                synset += '</inf:term>'

            print synset

    def __init__(self, file):
        self.getAllLabels()


a = WordnetTriples("../folder/bicycleauto_price_service.rdf")