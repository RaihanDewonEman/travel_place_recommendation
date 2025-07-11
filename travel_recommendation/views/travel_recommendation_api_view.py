from rest_framework.views import APIView
from rest_framework.response import Response
from travel_recommendation.models import District
from travel_recommendation.integration.air_quality_api import AirQualityAPI
from travel_recommendation.integration.weather_forecast_api import WeatherForecastAPI


class TravelRecommendationAPIView(APIView):

    def get(self, request):
        try:
            current_latitude = float(request.GET.get("current_latitude"))
            current_longitude = float(request.GET.get("current_longitude"))
            destination_name = request.GET.get("destination")
            travel_date = request.GET.get("travel_date")
        except Exception as e:
            return Response({"error": "current_latitude, current_longitude, destination, travel_date are required parameters!!!"}, status=404)

        try:
            destination = District.objects.get(name__iexact=destination_name)
        except District.DoesNotExist:
            return Response({"error": "Destination not found"}, status=404)

        def get_2pm_temperature(weather_data):
            for i, t in enumerate(weather_data["time"]):
                if t.startswith(travel_date) and t.endswith("14:00"):
                    return weather_data["temperature_2m"][i]
            return None

        def get_2pm_air_quality(air_quality_data):
            for i, t in enumerate(air_quality_data["time"]):
                if t.startswith(travel_date) and t.endswith("14:00"):
                    return air_quality_data["pm2_5"][i]
            return None

        try:
            _current_location_params = {"params": {
                "latitude": current_latitude,
                "longitude": current_longitude,
                "hourly": "temperature_2m",
                "timezone": "auto",
                "start_date": travel_date,
                "end_date": travel_date
            }}
            _destination_location_params = {"params": {
                "latitude": destination.latitude,
                "longitude": destination.longitude,
                "hourly": "temperature_2m",
                "timezone": "auto",
                "start_date": travel_date,
                "end_date": travel_date
            }}
            current_location_weather = WeatherForecastAPI.get_weather_forecast_data(**_current_location_params)
            destination_location_weather = WeatherForecastAPI.get_weather_forecast_data(**_destination_location_params)

            _current_location_params = {"params": {
                "latitude": current_latitude,
                "longitude": current_longitude,
                "hourly": "pm2_5",
                "timezone": "auto",
                "start_date": travel_date,
                "end_date": travel_date
            }}
            _destination_location_params = {"params": {
                "latitude": destination.latitude,
                "longitude": destination.longitude,
                "hourly": "pm2_5",
                "timezone": "auto",
                "start_date": travel_date,
                "end_date": travel_date
            }}
            current_location_air_quality = AirQualityAPI.get_air_quality_data(**_current_location_params)
            destination_location_air_quality = AirQualityAPI.get_air_quality_data(**_destination_location_params)

            current_location_temperature = get_2pm_temperature(current_location_weather["hourly"])
            destination_location_temperature = get_2pm_temperature(destination_location_weather["hourly"])

            current_location_air_quality_value = get_2pm_air_quality(current_location_air_quality["hourly"])
            destination_location_air_quality_value = get_2pm_air_quality(destination_location_air_quality["hourly"])

            recommendation = "Recommended" if destination_location_temperature < current_location_temperature and destination_location_air_quality_value < current_location_air_quality_value else "Not Recommended"

            if destination_location_temperature >= current_location_temperature:
                if destination_location_air_quality_value >= current_location_air_quality_value:
                    reason = "Your destination is hotter and has worse air quality than your current location. It's better to stay where you are."
                else:
                    reason = "Your destination is hotter but has significantly better air quality than your current location. It's better to stay where you are."
            else:
                if destination_location_air_quality_value >= current_location_air_quality_value:
                    reason = f"Your destination is {round(current_location_temperature - destination_location_temperature, 1)}°C cooler and has worse air quality than your current location. It's better to stay where you are."
                else:
                    reason = f"Your destination is {round(current_location_temperature - destination_location_temperature, 1)}°C cooler and has significantly better air quality. Enjoy your trip!"

            return Response({
                "recommendation": recommendation,
                "reason": reason
            })
        except Exception as e:
            print(e)
            return Response({"error": "Could not fetch weather data"}, status=500)
