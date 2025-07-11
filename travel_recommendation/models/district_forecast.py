from django.db import models
import datetime
from travel_recommendation.models import District


class DistrictForecast(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    weather_data = models.JSONField(null=True, blank=True)
    air_quality_data = models.JSONField(null=True, blank=True)
    api_call_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.district} : {self.api_call_date}"