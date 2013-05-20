__author__ = 'kuba'

from lxml import etree
import re

class WordnetTriples:

    host = "http://127.0.0.1/"

    def extractWords(self, pureLabel):
        words = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', pureLabel).split("_")
        #Remove empty string from list
        return filter(lambda a: a != '', words)

    def getAllLabels(self, file):
        document = etree.parse(file)
        results = document.xpath("//*/*/inf:hasLabel/@rdf:resource", namespaces={'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#", "inf":"http://127.0.0.1/inference#"  })
        for label in results:
            pureLabel = label[label.find("(")+1:-1]
            print self.extractWords(pureLabel)



    def __init__(self):
        self.getAllLabels("../folder/bicycleauto_price_service.rdf")
        # g = Graph()
        # g.load("../folder/bicycleauto_price_service.rdf")
        # url = URIRef("http://127.0.0.1")
        # for o in g.objects(url, INF.hasLabel):
        #     print s,p,o
        # parser = RDF.Parser(name="rdfxml")
        # model = RDF.Model()
        # stream = parser.parse_into_model(model,
        #                                  "file:///home/kuba/python/Cegla/Parser/folder/bicycleauto_price_service.rdf",
        #                                  "http://127.0.0.1/")
        # # for triple in model:
        # #     print "%s - %s - %s" % (triple.subject, triple.predicate,triple.object)
        #
        # q1 = RDF.Query("SELECT ?a WHERE (inf:hasLabel ?a)")
        # results = q1.execute(model)


a = WordnetTriples()