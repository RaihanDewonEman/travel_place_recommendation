import requests
from django.core.management.base import BaseCommand
from travel_recommendation.models.district import District
from travel_recommendation.config.constants import district_location_url

class Command(BaseCommand):
    def handle(self, *args, **options):
        response = requests.get(district_location_url)
        district_data = response.json()

        print("District data creation has started...")

        for district in district_data["districts"]:
            District.objects.get_or_create(id=district["id"], name=district["name"], latitude=district["lat"], longitude=district["long"])

        print("District data creation has finished.")