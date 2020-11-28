import handler
import json


def test_wind():
    response = handler.hello({
        "id": "way/222920036"
    }, {})
    payload_json = response['body']
    print(payload_json)
#    with open("test.png", "wb") as out:
#        out.write(payload_json)
#    assert 0 < len(json.loads(payload_json)['features'])
    assert "0 == 1"

test_wind()
