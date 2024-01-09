from rdflib import Graph, Literal
from rdflib.plugins.sparql import prepareQuery

# Carica il grafo RDF dal file
g = Graph()
g.parse("ItalyTravelApp_ontology.rdf", format="xml")  # Assicurati di specificare il formato corretto

# Definisci la query SPARQL per ottenere gli individui della classe Destination
query_string = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX myOnt: <http://www.semanticweb.org/agata/ontologies/2023/11/ItalyTravelApp_Ontology#>

SELECT DISTINCT ?placeName
WHERE {
  {
    ?city rdf:type myOnt:City ;
          myOnt:hasActivity ?activity .
    ?activity rdf:type myOnt:Skiing .
    BIND(strafter(str(?city), "#") as ?placeName)
  }
  UNION
  {
    ?village rdf:type myOnt:Village ;
             myOnt:hasActivity ?activity .
    ?activity rdf:type myOnt:Skiing .
    BIND(strafter(str(?village), "#") as ?placeName)
  }
  UNION
  {
    ?town rdf:type myOnt:Town ;
          myOnt:hasActivity ?activity .
    ?activity rdf:type myOnt:Skiing .
    BIND(strafter(str(?town), "#") as ?placeName)
  }
}
"""


# Prepara la query
query = prepareQuery(query_string)

# Esegui la query e stampa i risultati
results = g.query(query)
for row in results:
    print(row.placeName)
