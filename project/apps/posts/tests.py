from django.test import TestCase, Client
from django.db import IntegrityError
from project.apps.categories.models import Category, Subcategory
from project.apps.posts.models import Posts
import json

class PostsTestViewCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Category 1')
        self.subcategory = Subcategory.objects.create(name='Category 1', category=self.category)
    
    def test_post_create_ok(self):
        response = self.client.post ('/posts/', {
            "title":"Post 1",
            "prev":"Previously...",
            "body":"This is a story...",
            "tags":json.dumps({'tag': 'sometag'}),
            "category":self.category.id,
            "subcategory":self.subcategory.id
        })

        self.assertEquals(response.status_code, 201)
    
    def test_post_create_bad_request(self):
        response = self.client.post ('/posts/', {
            "badtitle":"Bad Post",
        })

        self.assertEquals(response.status_code, 400)
    
    def test_post_create_repeated_title(self):
        self.client.post ('/posts/', {
            "title":"Post 1",
            "prev":"Previously...",
            "body":"This is a story...",
            "tags":json.dumps({'tag': 'sometag'}),
            "category":self.category.id,
            "subcategory":self.subcategory.id
        })

        with self.assertRaises(IntegrityError):
            self.client.post ('/posts/', {
                "title":"Post 1",
                "prev":"Previously...",
                "body":"This is a story...",
                "tags":json.dumps({'tag': 'sometag'}),
                "category":self.category.id,
                "subcategory":self.subcategory.id
            })
    
    def test_post_list_empty_ok(self):
        response = self.client.get ('/posts/')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.content),2)
    
    def test_post_list_with_content_ok(self):
        self.client.post ('/posts/', {
            "title":"Post 1",
            "prev":"Previously...",
            "body":"This is a story...",
            "tags":json.dumps({'tag': 'sometag'}),
            "category":self.category.id,
            "subcategory":self.subcategory.id
        })
        self.client.post ('/posts/', {
            "title":"Post 2",
            "prev":"Previously...",
            "body":"This is a second story...",
            "tags":json.dumps({'tag': 'sometag'}),
            "category":self.category.id,
            "subcategory":self.subcategory.id
        })
        response = self.client.get ('/posts/')

        self.assertEquals(response.status_code, 200)
        self.assertGreater(len(response.content),2)