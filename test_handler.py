import geojson
import handler
import json


def grove_nursery_recycling_centre():
    grove_nursery = {"id": "way/488949555"}
    response = handler.boundary(grove_nursery, {})
    payload_json = response['body']
    print(payload_json)
    assert "0 == 1"

def kirkby_moor_wind_farm():
    kirkby_moor = {"id": "relation/2928690"}
    response = handler.boundary(kirkby_moor, {})
    payload_json = response['body']
    print(payload_json)

def bridge_of_don_recycling_centre():
    bridge_of_don = {"id": "way/590188051"}
    response = handler.boundary(bridge_of_don, {})
    payload_json = response['body']
    print(payload_json)

def hazlehead_recycling_centre():
    hazlehead = {"id": "way/488949555"}
    response = handler.boundary(hazlehead, {})
    payload_json = response['body']
    print(payload_json)

def aberdeen():
    grove_nursery = {"id": "way/488949555"}
    bridge_of_don = {"id": "way/590188051"}
    hazlehead = {"id": "way/488949555"}
    aberdeen = [grove_nursery, bridge_of_don, hazlehead]
    features = []
    for site in aberdeen:
        response = handler.boundary(site, {})
        payload_json = response['body']
        feature = geojson.Feature(payload_json)
        features.append(feature)
    feature_collection = geojson.FeatureCollection(features)
    with open('HWRC.geojson', 'w') as f:
        f.write(geojson.dumps(feature_collection, indent=2))

aberdeen()
