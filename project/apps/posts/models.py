from django.db import models
from django.contrib.postgres.fields import JSONField
from django.template.defaultfilters import slugify
from project.common.models import FieldDefaultsAbstracts
from project.apps.categories.models import Category, Subcategory

class Posts(FieldDefaultsAbstracts):
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250, unique=True)
    prev = models.CharField(max_length=250, null=True)
    body = models.TextField()
    tags = JSONField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Posts, self).save(*args, **kwargs)