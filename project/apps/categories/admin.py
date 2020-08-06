from django.contrib import admin
from project.apps.categories.models import Category, Subcategory

admin.site.register(Category)
admin.site.register(Subcategory)