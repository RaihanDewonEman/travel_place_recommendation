import datetime
from django.core.management.base import BaseCommand

from travel_recommendation.models import DistrictForecast
from travel_recommendation.models.district import District
from travel_recommendation.integration.air_quality_api import AirQualityAPI
from travel_recommendation.integration.weather_forecast_api import WeatherForecastAPI

class Command(BaseCommand):
    def handle(self, *args, **options):
        districts = District.objects.all()
        cnt = 0
        print("District forecast data fetching has started...")
        for district in districts:
            district_forecast, created = DistrictForecast.objects.get_or_create(district=district,
                                                                                api_call_date=datetime.date.today())
            _params = {"latitude": district.latitude, "longitude": district.longitude}

            try:
                weather_data = WeatherForecastAPI.get_weather_forecast_data(**_params)
                district_forecast.weather_data = weather_data
                district_forecast.save()
            except Exception as e:
                print(e)
                continue

            try:
                air_quality_data = AirQualityAPI.get_air_quality_data(**_params)
                district_forecast.air_quality_data = air_quality_data
                district_forecast.save()
            except Exception as e:
                print(e)
                continue
            cnt += 1
            if cnt%5 == 0:
                print("District forecast data fetching is running...")
        print("District forecast data fetching has completed.".format(cnt))