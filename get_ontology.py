from rdflib import Graph, Literal
from rdflib.plugins.sparql import prepareQuery

# Carica il grafo RDF dal file
g = Graph()
g.parse("ItalyTravelApp_ontology.rdf", format="xml")  # Assicurati di specificare il formato corretto

# Definisci la query SPARQL per ottenere gli individui della classe Destination
query_string = """
SELECT ?destination
WHERE {
   ?destination a <http://www.w3.org/2002/07/owl#Class>.
}
"""

# Prepara la query
query = prepareQuery(query_string)

# Esegui la query e stampa i risultati
results = g.query(query)
for row in results:
   print(row.destination)
