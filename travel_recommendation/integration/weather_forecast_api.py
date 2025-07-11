import requests

from travel_recommendation.config.constants import weather_api_domain_name, weather_api_endpoint


class WeatherForecastAPI:

    @classmethod
    def prepare_get_api_url(cls, **kwargs):
        _api_url = "{api_domain_name}/{api_endpoint}".format(
            api_domain_name=weather_api_domain_name,
            api_endpoint=weather_api_endpoint,
        )

        return _api_url

    @classmethod
    def get_weather_forecast_data(cls, **kwargs):
        url = cls.prepare_get_api_url(**kwargs)
        _params = kwargs["params"]
        response = requests.get(url, params=_params)
        return response.json()
