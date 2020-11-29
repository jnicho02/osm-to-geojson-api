import json
from qwikidata.sparql import return_sparql_query_results

class Wikidata():

    def __init__(self, wikidata_id: str):
        self.wikidata_id = wikidata_id
        query_string = """
                SELECT ?operatorLabel ?image
                WHERE 
                {
                  BIND( <http://www.wikidata.org/entity/%s> as ?recycling_centre )
                  OPTIONAL { ?recycling_centre wdt:P18 ?image. }
                  OPTIONAL { ?recycling_centre wdt:P137 ?operator. }
                  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
                }""" % (wikidata_id)
        res = return_sparql_query_results(query_string)
        props = res["results"]["bindings"][0]
        self.properties = {}
        for key in props.keys():
          self.properties[key.replace('Label','')] = props[key]['value']


w = Wikidata('Q102132154')
print(w.properties)



recycling_centres = """
        SELECT ?item ?itemLabel
        WHERE
        {
          ?item wdt:P31 wd:Q27106436.
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }"""



