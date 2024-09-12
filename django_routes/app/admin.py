from django.contrib import admin
from .models import Route

class RouteAdmin(admin.ModelAdmin):
    
    search_fields = ['route_id']  
    list_filter = ['route_short_name']  
    list_display = ['route_id', 'route_short_name', 'route_long_name']

admin.site.register(Route, RouteAdmin)
