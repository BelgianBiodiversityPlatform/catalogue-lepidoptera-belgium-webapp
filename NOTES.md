Tip: Sparql to get Wikidata info on a family:
=============================================

SELECT ?item ?itemLabel WHERE {
  ?item rdfs:label "Eriocraniidae"@en.
  ?item wdt:P105 wd:Q35409.
}

?item wdt:P105 wd:Q35409. => taxon rank is family