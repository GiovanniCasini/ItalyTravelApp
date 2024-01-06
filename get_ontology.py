from rdflib import Graph, Literal
from rdflib.plugins.sparql import prepareQuery

# Carica il grafo RDF dal file
g = Graph()
g.parse("ItalyTravelApp_ontology.rdf", format="xml")  # Assicurati di specificare il formato corretto

def get_destinations():
   # Definisci la query SPARQL per ottenere gli individui della classe Destination
   query_string = """
   PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
   PREFIX owl: <http://www.w3.org/2002/07/owl#>
   PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
   PREFIX myOnt: <http://www.semanticweb.org/agata/ontologies/2023/11/ItalyTravelApp_Ontology#>

   SELECT (strafter(str(?individual), "#") as ?individualName)
   WHERE {
      ?subclass rdf:type owl:Class ;
               rdfs:subClassOf* myOnt:Destination .
      
      ?individual rdf:type ?subclass .
   }
   """
   query = prepareQuery(query_string)
   results = g.query(query)
   #for row in results:
      #print(row.individualName)

   dests = []
   for row in results:
      dests.append(row)
   return dests


def get_activities():
   # Definisci la query SPARQL per ottenere gli individui della classe Destination
   query_string = """
   PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
   PREFIX owl: <http://www.w3.org/2002/07/owl#>
   PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
   PREFIX myOnt: <http://www.semanticweb.org/agata/ontologies/2023/11/ItalyTravelApp_Ontology#>

   SELECT
   (strafter(str(?predicate), "#") as ?predicateName)
   (strafter(str(?relatedIndividual), "#") as ?relatedIndividualName)
   WHERE {
   myOnt:Florence ?predicate ?relatedIndividual.
   }
   """
   query = prepareQuery(query_string)
   results = g.query(query)
   #for row in results:
      #print(row.individualName)

   activities = []
   for row in results:
      activities.append(row)
   return activities

