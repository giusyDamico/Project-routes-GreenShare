from django.urls import path
from . import views
from .views import RouteListAPIView
from django.conf.urls import handler404
from .views import custom_page_not_found_view

handler404 = 'app.views.custom_page_not_found_view'


urlpatterns = [
    path('upload-routes/',views.upload_routes, name='upload-routes'),
    path('import-file/', views.import_routes_from_url, name='import-file'),
    path('view-routes/', views.view_routes, name = 'view-routes'),
    path('routes/', RouteListAPIView.as_view(), name='route-list'),  
    path('refresh-db/', views.refresh_db, name='refresh-db'),  
]
