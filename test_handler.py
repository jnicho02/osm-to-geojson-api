import geojson
import handler
import json


def grove_nursery_recycling_centre():
    grove_nursery = {"path": "/way/488949555"}
    response = handler.boundary(grove_nursery, {})
    payload_json = response['body']
    print(payload_json)

def kirkby_moor_wind_farm():
    kirkby_moor = {"path": "/relation/2928690"}
    response = handler.boundary(kirkby_moor, {})
    payload_json = response['body']
    print(payload_json)

def bridge_of_don_recycling_centre():
    bridge_of_don = {"path": "/way/590188051"}
    response = handler.boundary(bridge_of_don, {})
    payload_json = response['body']
    print(payload_json)

def hazlehead_recycling_centre():
    hazlehead = {"path": "/way/488949555"}
    response = handler.boundary(hazlehead, {})
    payload_json = response['body']
    print(payload_json)

def aberdeen():
    grove_nursery = {"path": "/way/488949555"}
    bridge_of_don = {"path": "/way/590188051"}
    hazlehead = {"path": "/way/488949555"}
    all_of_them = [grove_nursery, bridge_of_don, hazlehead,
        {"path": "node/2300250889"},
        {"path": "/way/468144801"},
        {"path": "/way/878868635"},
        {"path": "node/2921781304"},
        {"path": "node/4610434492"},
        {"path": "/way/878867808"},
        {"path": "/way/100783605"},
        {"path": "/way/248336564"},
        {"path": "/way/476694225"},
        {"path": "/way/878867009"},
        {"path": "/way/473816199"},
        {"path": "/way/878865764"},
        {"path": "/way/41958866"},
        {"path": "/way/116883204"},
        {"path": "/way/878914414"},
        {"path": "/way/878917216"}
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

bridge_of_don_recycling_centre()
