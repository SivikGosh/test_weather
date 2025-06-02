from unittest.mock import patch

from src.utils import get_coordinates, get_weather


@patch('src.utils.requests.get')
def test_get_coordinates_success(mock_get):
    mock_get.return_value.json.return_value = [{
        'lat': '55.7558',
        'lon': '37.6173'
    }]

    lat, lon = get_coordinates('Moscow')
    assert lat == 55.7558
    assert lon == 37.6173
    mock_get.assert_called_once()


@patch('src.utils.requests.get')
def test_get_coordinates_empty_response(mock_get):
    mock_get.return_value.json.return_value = []

    lat, lon = get_coordinates('UnknownCity')
    assert lat is None
    assert lon is None


@patch('src.utils.requests.get')
def test_get_weather_success(mock_get):
    mock_get.return_value.json.return_value = {
        'current_weather': {
            'temperature': 21.5,
            'windspeed': 5.2
        }
    }

    result = get_weather(55.7558, 37.6173)
    assert 'current_weather' in result
    assert result['current_weather']['temperature'] == 21.5
    mock_get.assert_called_once()
