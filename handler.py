from osm_site import OsmSite


def hello(event, context):
    site = OsmSite(event['id'])

    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/geo+json',
        },
        'body': site.feature()
    }

    return response
