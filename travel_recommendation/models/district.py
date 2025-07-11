from django.db import models

class District(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"id {self.id}: {self.name}"