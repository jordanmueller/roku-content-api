"""
Model tests
"""

from django.test import TestCase
from django.db import IntegrityError
from library.models import Category, Course, Lecture

class ModelTests(TestCase):
    def setUp(self):
        Category.objects.create(category_type="computer science")
        category = Category.objects.get(category_type="computer science")
        Course.objects.create(categories=category)

    def test_category_model(self):
        """
        Tests that the category type returns a category
        """
        category = Category.objects.get(category_type="computer science")
        self.assertEqual(category.category_type, 'computer science')

    def test_duplicate_entry(self):
        """
        Tests that we cannot entry duplicate categories
        """
        with self.assertRaises(IntegrityError):
            Category.objects.create(category_type="computer science")
