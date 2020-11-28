import handler
import json


def test_wind():
    grove_nursery_recycling_centre = {"id": "way/488949555"}
    kirkby_moor_wind_farm = {"id": "relation/2928690"}
    response = handler.hello(grove_nursery_recycling_centre, {})
    payload_json = response['body']
    print(payload_json)
    assert "0 == 1"

test_wind()
