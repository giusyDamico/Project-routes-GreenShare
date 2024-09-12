from django.db import models

class Route(models.Model):
    route_id = models.CharField(max_length=10)
    agency_id = models.CharField(max_length=10)
    route_short_name = models.CharField(max_length=50)
    route_long_name = models.CharField(max_length=100)
    route_desc = models.TextField(blank=True, null=True)
    route_type = models.IntegerField()
    route_url = models.URLField()
    route_color = models.CharField(max_length=6)
    route_text_color = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.route_short_name} - {self.route_long_name}"
