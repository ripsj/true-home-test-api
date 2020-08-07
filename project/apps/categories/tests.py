from django.test import TestCase, Client
from project.apps.categories.models import Category, Subcategory

class CategoryTestViewCase(TestCase):
    def setUp(self):
        self.client = Client()