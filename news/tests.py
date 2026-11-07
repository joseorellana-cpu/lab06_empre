from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, Author, Category


class PortalTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name='Test Author')
        self.category = Category.objects.create(name='Tech', slug='tech')
        self.article = Article.objects.create(
            title='Hello', summary='Short summary', body='<b>bold</b>',
            published_at=timezone.now(), author=self.author,
        )
        self.article.categories.add(self.category)

    def test_home_lists_articles(self):
        response = self.client.get(reverse('news:home'))
        self.assertContains(response, 'Hello')

    def test_home_empty_case(self):
        Article.objects.all().delete()
        response = self.client.get(reverse('news:home'))
        self.assertContains(response, 'Todavía no hay noticias')

    def test_detail_page(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertContains(response, 'Test Author')

    def test_category_page_reuses_card(self):
        response = self.client.get(reverse('news:category', args=['tech']))
        self.assertContains(response, 'Hello')

    def test_html_in_body_is_escaped(self):
        response = self.client.get(self.article.get_absolute_url())
        self.assertContains(response, '&lt;b&gt;bold&lt;/b&gt;')
        self.assertNotContains(response, '<b>bold</b>')

    def test_unknown_article_returns_404(self):
        self.assertEqual(self.client.get(reverse('news:detail', args=[999])).status_code, 404)

    def test_static_stylesheet_is_linked(self):
        response = self.client.get(reverse('news:home'))
        self.assertContains(response, '/static/css/style.css')
