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
    all_of_them = [grove_nursery, bridge_of_don, hazlehead,
        {"id": "node/2300250889"},
        {"id": "node/1453597969"},
        {"id": "way/468144801"},
        {"id": "way/878868635"},
        {"id": "node/2921781304"},
        {"id": "node/4610434492"},
        {"id": "way/878867808"},
        {"id": "way/100783605"},
        {"id": "way/248336564"},
        {"id": "way/476694225"},
        {"id": "way/878867009"},
        {"id": "way/473816199"},
        {"id": "way/878865764"},
        {"id": "way/41958866"},
        {"id": "way/116883204"},
        {"id": "way/878914414"}
    ]
    features = []
    for site in all_of_them:
        response = handler.boundary(site, {})
        payload_json = response['body']
        feature = geojson.Feature(
            geometry = payload_json['geometry'],
            properties = payload_json['properties']
        )
        features.append(feature)
    feature_collection = geojson.FeatureCollection(features)
    import os
    if os.path.exists('HWRC.geojson'):
        os.remove('HWRC.geojson')
    with open('HWRC.geojson', 'w') as f:
        f.write(geojson.dumps(feature_collection, indent=2))

aberdeen()
