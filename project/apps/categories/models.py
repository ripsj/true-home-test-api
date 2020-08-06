from django.db import models
from project.common.models import FieldDefaultsAbstracts
from django.template.defaultfilters import slugify

class Category(FieldDefaultsAbstracts):
    name = models.CharField(max_length=75)
    slug = models.CharField(max_length=75, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Subcategory(FieldDefaultsAbstracts):
    name = models.CharField(max_length=75)
    slug = models.CharField(max_length=75, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)