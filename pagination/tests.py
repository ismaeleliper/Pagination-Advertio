from django.test import TestCase
from pagination.views import Pagination
from pagination.models import Text


class PaginationTestCase(TestCase):
    def setUp(self):
        Text.objects.create(id=2, description="My first text").save()

    def test_split_result(self):
        generator = Pagination(limit=1, model_class=Text)._split_result()
        self.assertEqual(next(generator), [{'description': 'My first text', 'id': 2}])

    def test_split_result_exception(self):
        generator = Pagination(limit=1, model_class=TestCase)._split_result()  # Using a wrong class
        self.assertRaises(Exception, generator)

    def test_num_of_pages(self):
        num = Pagination(limit=1, model_class=Text).num_of_pages()
        self.assertEqual(num, 1)

    def test_num_of_pages_equal_zero(self):
        Text.objects.get(id=2).delete()
        num = Pagination(limit=1, model_class=Text).num_of_pages()
        self.assertEqual(num, 1)

    def test_num_of_exception(self):
        with self.assertRaises(Exception):
            Pagination(limit=1, model_class=TestCase).num_of_pages()

    def test_result_by_limit(self):
        # Total of Texts == 4
        Text.objects.create(id=3, description="My second text").save()
        Text.objects.create(id=4, description="My third text").save()
        Text.objects.create(id=5, description="My fourth text").save()

        # limit of results (2) divided by each page is equal 2 result per page.
        result_page_1 = Pagination(limit=2, model_class=Text).result(number_of_page_choosen=1)
        self.assertEqual(len(result_page_1), 2)

        # limit of results (4) divided by each page is equal 1 result per page.
        result_page_1 = Pagination(limit=4, model_class=Text).result(number_of_page_choosen=1)
        self.assertEqual(len(result_page_1), 4)

    def test_result_by_limit_exception(self):
        with self.assertRaises(Exception):
            Pagination(limit=4, model_class=TestCase).result(number_of_page_choosen=1)


class PaginationAppTestCase(TestCase):
    def setUp(self):
        Text.objects.create(id=2, description="My first text").save()

    def test_model_text(self):
        text = Text.objects.first()
        self.assertEqual(text.description, "My first text")
        self.assertEqual(text.pk, 2)

    def test_view_pagination(self):
        response = self.client.get('http://localhost:8000/text?page=1&limit=1')
        self.assertEqual(response.status_code, 200)

    def test_view_pagination_exception(self):
        response = self.client.get('http://localhost:8000/text?page=1')
        self.assertEqual(response.status_code, 400)
