from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Route

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.upload_url = reverse('upload-routes')
        self.import_url = reverse('import-file')
        self.view_routes_url = reverse('view-routes')
        self.refresh_db_url = reverse('refresh-db')

    def test_view_routes(self):
        Route.objects.create(
            route_id='1',
            agency_id='Agency',
            route_short_name='ShortName',
            route_long_name='LongName',
            route_desc='Description',
            route_type=1,
            route_url='http://example.com',
            route_color='FFFFFF',  
            route_text_color='000000'  
        )
        response = self.client.get(self.view_routes_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view.html')
        self.assertContains(response, 'ShortName')
        self.assertContains(response, 'LongName')

    def test_import_routes_from_url(self):
        file_url = 'https://www.ctmcagliari.it/open_data/GTFS.zip'
        response = self.client.post(self.import_url, {'file_url': file_url})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.view_routes_url)

    def test_upload_routes(self):
        
        test_file = SimpleUploadedFile(
            "routes.txt", 
            b"route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color\n1,Agency,ShortName,LongName,,1,http://example.com,FFFFFF,000000"
        )
        
        response = self.client.post(self.upload_url, {'file': test_file})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.view_routes_url)
        
      
        self.assertTrue(Route.objects.filter(route_id='1').exists())

    def test_refresh_db(self):
        
        Route.objects.create(
            route_id='1',
            agency_id='Agency',
            route_short_name='ShortName',
            route_long_name='LongName',
            route_desc='Description',
            route_type=1,
            route_url='http://example.com',
            route_color='FFFFFF',  
            route_text_color='000000'  
        )
        response = self.client.get(self.refresh_db_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'refresh_db.html')
        self.assertEqual(Route.objects.count(), 0)  

    def test_custom_404_page(self):
        response = self.client.get('/non-existent-url/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
