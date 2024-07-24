import pytest
from rest_framework import status


def test_api_parse_succeeds(client):
    # TODO: Finish this test. Send a request to the API and confirm that the
    # data comes back in the appropriate format.
    address_string = '123 main st chicago il'
    response = client.get(
        "/api/parse/",
        {"address": address_string},
    )
    assert response.status_code == 200

    expected_dict = dict({
        "input_string": address_string,
        "address_components": {
            "AddressNumber": "123",
            "StreetName": "main",
            "StreetNamePostType": "st",
            "PlaceName": "chicago",
            "StateName": "il"
        },
        "address_type": "Street Address"
    })

    if response.json()['data'] is None:
        pytest.fail()

    assert response.json()['data'] == expected_dict


def test_api_parse_raises_error(client):
    # TODO: Finish this test. The address_string below will raise a
    # RepeatedLabelError, so ParseAddress.parse() will not be able to parse it.
    address_string = '123 main st chicago il 123 main st'
    response = client.get('/api/parse/', {"address": address_string})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    if response.json()['data'] is not None:
        pytest.fail()

    response = client.get('/api/parse/', {"city": address_string})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    if response.json()['data'] is not None:
        pytest.fail()
