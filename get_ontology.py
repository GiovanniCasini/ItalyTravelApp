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

   names = [str(result[0]).replace('_', ' ') for result in results]
   return names


def get_activities(destination):
   # Definisci la query SPARQL per ottenere gli individui della classe Destination
   query_string = f"""
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      PREFIX owl: <http://www.w3.org/2002/07/owl#>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      PREFIX myOnt: <http://www.semanticweb.org/agata/ontologies/2023/11/ItalyTravelApp_Ontology#>

      SELECT
      (strafter(str(?predicate), "#") as ?predicateName)
      (strafter(str(?relatedIndividual), "#") as ?relatedIndividualName)
      WHERE {{
         myOnt:{destination} ?predicate ?relatedIndividual.
      }}
   """

   query = prepareQuery(query_string)
   results = g.query(query)

   activities = []
   is_similar_to = ""
   for row in results:
      if row[0] == Literal('hasActivity'):
        activity_name = str(row[1]).replace('_', ' ')
        activities.append(activity_name)
      if row[0] == Literal('isSimilarTo'):
        sim = str(row[1]).replace('_', ' ')
        is_similar_to = sim
   return activities, is_similar_to
