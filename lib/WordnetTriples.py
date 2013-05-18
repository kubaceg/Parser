__author__ = 'kuba'

import libxml2 as xml
import re

class WordnetTriples:

    labels = []

    def getAllLabels(self, file):
        document = xml.parseDoc(open(file).read())
        context = document.xpathNewContext()
        context.xpathRegisterNs("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        context.xpathRegisterNs("inf", "http://127.0.0.1/inference#")
        results = context.xpathEval("//*/*/inf:hasLabel/@rdf:resource")
        for label in results:
            pureLabel = label.content[label.content.find("(")+1:-1]
            print re.sub('(.)([A-Z][a-z]+)', r'\1_\2', pureLabel).lower().split("_")


    def __init__(self):
        self.getAllLabels("../folder/bicycleauto_price_service.rdf")
        print self.labels
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