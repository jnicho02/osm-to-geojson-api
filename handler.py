import json
from osm_site import OsmSite
from wikidata import Wikidata


def boundary(event, context):
    id = event['path']
    site = OsmSite(id)
    if 'wikidata' in site.properties:
        wikidata_id = site.properties['wikidata']
        wikidata = Wikidata(wikidata_id)
        site.update(wikidata.properties)

    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/geo+json',
        },
        'body': json.dumps(site.feature_collection())
    }

    return response
