import requests

from travel_recommendation.config.constants import air_quality_api_endpoint, air_quality_api_domain_name

class AirQualityAPI:

    @classmethod
    def prepare_get_api_url(cls, **kwargs):
        _api_url = "{api_domain_name}/{api_endpoint}".format(
            api_domain_name=air_quality_api_domain_name,
            api_endpoint=air_quality_api_endpoint,
        )

        return _api_url

    @classmethod
    def get_air_quality_data(cls, **kwargs):
        url = cls.prepare_get_api_url(**kwargs)
        _params = {
            "latitude": kwargs["latitude"],
            "longitude": kwargs["longitude"],
            "hourly": "pm2_5",
            "timezone": "auto"
        }
        response = requests.get(url, params=_params)
        return response.json()