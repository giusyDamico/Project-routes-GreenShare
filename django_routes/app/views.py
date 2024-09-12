import csv
import requests
import os
import zipfile
import io
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.files.storage import default_storage
from app.models import Route  
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .serializers import RouteSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view



def view_routes(request):
    routes = Route.objects.all()  # take all routes from DB
    message = request.session.pop('message', '')  # take and refresh message
    return render(request, 'view.html', {'routes': routes, 'message': message})

class RouteListAPIView(generics.ListAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['route_long_name', 'route_id']
    permission_classes=[IsAuthenticated]

@api_view(['POST'])
def import_routes_from_url(request):
    # Obtain url from query
    file_url = request.data.get('file_url', None)

    if file_url:
       
        try:
            response = requests.get(file_url)
            if response.status_code == 200:
                if file_url.endswith('.zip'):
                    # extraction of file routes.txt from .ZIP
                    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
                    if 'routes.txt' not in zip_file.namelist():
                        return Response({"error": "The file .ZIP must have: routes.txt."}, status=400)

                    with zip_file.open('routes.txt') as file:
                        file_path = default_storage.save('routes_from_url.txt', file)

                elif file_url.endswith('.txt'):
                    # save file .txt 
                    file_path = default_storage.save('routes_from_url.txt', io.BytesIO(response.content))
                else:
                    return Response({"error": "Only file .txt o .zip are supported."}, status=400)
            else:
                return Response({"error": "Error during download."}, status=400)
        except Exception as e:
            return Response({"error": f"Error during request: {str(e)}"}, status=500)
    else:
        return Response({"error": "No URL is given."}, status=400)

    # Insert data on DB
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        route_count = 0
        for row in reader:
            Route.objects.update_or_create(
                route_id=row['route_id'],
                defaults={
                    'agency_id': row['agency_id'],
                    'route_short_name': row['route_short_name'],
                    'route_long_name': row['route_long_name'],
                    'route_desc': row.get('route_desc', ''),
                    'route_type': row['route_type'],
                    'route_url': row['route_url'],
                    'route_color': row['route_color'],
                    'route_text_color': row['route_text_color']
                }
            )
            route_count += 1

    # Delete the temporarly file
    default_storage.delete(file_path)

     # Redirect to the view_routes page with a success message
    request.session['message'] = f'Successfully imported {route_count} routes.'
    return HttpResponseRedirect('/app/view-routes/')

def upload_routes(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file', None)

        # Check if the uploaded file is .zip
        if uploaded_file.name.endswith('.zip'):
            # Save the file
            zip_path = default_storage.save('temp_routes.zip', uploaded_file)
            full_zip_path = default_storage.path(zip_path)  # Take the full path
            # Extraction of 'routes.txt' from file ZIP
            with zipfile.ZipFile(full_zip_path, 'r') as zip_ref:
                if 'routes.txt' not in zip_ref.namelist():
                    default_storage.delete(full_zip_path)
                    return render(request, 'upload.html', {'message': 'The ZIP file must contain routes.txt.'})

                # Extraction of 'routes.txt'
                zip_ref.extract('routes.txt', default_storage.location)

            # Path of routes.txt
            file_path = os.path.join(default_storage.location, 'routes.txt')

            # Delete file ZIP 
            default_storage.delete(full_zip_path)

        
        elif uploaded_file.name == 'routes.txt':
           
            file_path = default_storage.save('temp_routes.txt', uploaded_file)
            file_path = default_storage.path(file_path)  

        else:
            return render(request, 'upload.html', {'message': 'Please upload a routes.txt file or a ZIP containing routes.txt.'})

        # Read the routes.txt file and import data
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            route_count = 0
            for row in reader:
                Route.objects.update_or_create(
                    route_id=row['route_id'],
                    defaults={
                        'agency_id': row['agency_id'],
                        'route_short_name': row['route_short_name'],
                        'route_long_name': row['route_long_name'],
                        'route_desc': row.get('route_desc', ''),
                        'route_type': row['route_type'],
                        'route_url': row['route_url'],
                        'route_color': row['route_color'],
                        'route_text_color': row['route_text_color']
                    }
                )
                route_count += 1

        # Delete file 
        default_storage.delete(file_path)

        # Redirect to the view_routes page with a success message
        request.session['message'] = f'Successfully imported {route_count} routes.'
        return HttpResponseRedirect('/app/view-routes/')
    
    return render(request, 'upload.html')


def custom_page_not_found_view(request, exception):
    return render(request, '404.html',status=404)

def refresh_db(request):
    Route.objects.all().delete() 
    return render(request, 'refresh_db.html')