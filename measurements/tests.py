from urllib import response
from django.test import TestCase
from django.urls import reverse
from .models import Measurement
from users.models import User

def create_measurement(weight, fat_percentage, muscle_percentage, calories, user):
    m = Measurement.objects.create(weight=weight, fat_percentage=fat_percentage, muscle_percentage=muscle_percentage, calories=calories, user=user)
    return m

# Create your tests here.
class MeasurementIndexViewTests(TestCase):
    
    def test_no_measurements(self):
        """
        If no measurements exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No measurements were found.")
        self.assertQuerysetEqual(response.context['latest_measurement_list'], [])
        
    
    def test_one_measurement(self):
        """
        Should return the latest measurement for a user
        """
        measurement1 = create_measurement(weight=80, fat_percentage=10, muscle_percentage=20, calories=1000, user=User.objects.create_user(username='testuser1'))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_measurement_list'], [measurement1])
        
        
    def test_multiple_measurement(self):
        """
        Should return the latest measurements for a user
        """
        measurement1 = create_measurement(weight=80, fat_percentage=10, muscle_percentage=20, calories=1000, user=User.objects.create_user(username='testuser1'))
        measurement2 = create_measurement(weight=80, fat_percentage=10, muscle_percentage=20, calories=1000, user=User.objects.create_user(username='testuser2'))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_measurement_list'], [ measurement2, measurement1])
        
class MeasurementDetailsViewTests(TestCase):
    
    def test_no_measurement(self):
        """
        Should return 404 if no measurement is found
        """
        response = self.client.get(reverse('detail', args=(1,)))
        self.assertEqual(response.status_code, 404)
    
        
    def test_measurement(self):
        """
        Should return the required measurement
        """
        measurement1 = create_measurement(weight=80, fat_percentage=10, muscle_percentage=20, calories=1000, user=User.objects.create_user(username='testuser1'))
        response = self.client.get(reverse('detail', args=(measurement1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "80")
        self.assertContains(response, "10")
        self.assertContains(response, "20")
        self.assertContains(response, "1000")
        