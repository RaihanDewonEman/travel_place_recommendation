import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Prefetch
from travel_recommendation.models import District, DistrictForecast


class DistrictAPIView(APIView):

    def get(self, request):
        today = datetime.date.today()
        district_list = []
        best_districts = {}
        districts_with_forecast = District.objects.prefetch_related(
            Prefetch(
                'districtforecast_set',
                queryset=DistrictForecast.objects.filter(api_call_date=today),
                to_attr='today_forecast'
            )
        )

        for district in districts_with_forecast:
            if district.today_forecast:
                forecast = district.today_forecast[0]
                weather_time = forecast.weather_data["hourly"]["time"]
                weather_temperature = forecast.weather_data["hourly"]["temperature_2m"]
                air_quality_pm2_5 = forecast.air_quality_data["hourly"]["pm2_5"]

                seven_days_temperature = [weather_temperature[i] for i, t in enumerate(weather_time) if t.endswith("14:00")]
                avg_temperature = sum(seven_days_temperature) / len(seven_days_temperature)
                air_quality = sum(air_quality_pm2_5) / len(air_quality_pm2_5)

                district_list.append({
                    "id": district.id,
                    "name": district.name,
                    "latitude": district.latitude,
                    "longitude": district.longitude,
                    "avg_temperature": avg_temperature,
                    "air_quality_index": air_quality,
                })
                best_districts = sorted(district_list, key=lambda x: (x["avg_temperature"], x["air_quality_index"]))[:10]

        return Response(best_districts)