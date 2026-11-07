from datetime import timedelta
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from PIL import Image, ImageDraw

from news.models import Article, Author, Category

CATEGORIES = [('Tecnología', 'tecnologia'), ('Deportes', 'deportes'), ('Cultura', 'cultura')]
COLORS = ['#0b5ed7', '#198754', '#d63384', '#fd7e14', '#6f42c1', '#20c997']

# Step 12: this body is stored as HTML on purpose. Django's auto-escaping must
# show the tags as literal text in the detail page (no bold, no alert()).
HTML_BODY = (
    'Este párrafo contiene <b>negrita</b> y un <script>alert(1)</script> guardados tal cual.\n\n'
    'Si la página los ejecutara, el navegador pondría la negrita y lanzaría el diálogo.'
)

ARTICLES = [
    ('Nueva línea de buses eléctricos en Lima', ['tecnologia'], 'Ana Torres'),
    ('Inteligencia artificial en las aulas peruanas', ['tecnologia', 'cultura'], 'Ana Torres'),
    ('La selección clasifica a la siguiente ronda', ['deportes'], 'Luis Paredes'),
    ('Maratón de Lima rompe récord de inscritos', ['deportes'], 'Luis Paredes'),
    ('Festival de cine reúne a nuevos directores', ['cultura'], 'Ana Torres'),
    ('Prueba de escapado: <b>negrita</b> y <script>alert(1)</script>', ['cultura', 'tecnologia'], 'Luis Paredes'),
]


def make_image(color, label):
    """Build a simple colored banner so articles have a featured image."""
    image = Image.new('RGB', (800, 500), color)
    ImageDraw.Draw(image).text((30, 30), label, fill='white')
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = 'Load sample authors, categories and six articles for the portal.'

    def handle(self, *args, **options):
        categories = {slug: Category.objects.get_or_create(name=name, slug=slug)[0]
                      for name, slug in CATEGORIES}
        authors = {
            'Ana Torres': Author.objects.get_or_create(
                name='Ana Torres', defaults={'email': 'ana@example.com', 'bio': 'Periodista de tecnología y cultura.'})[0],
            'Luis Paredes': Author.objects.get_or_create(
                name='Luis Paredes', defaults={'email': 'luis@example.com', 'bio': 'Redactor deportivo.'})[0],
        }
        now = timezone.now()
        for index, (title, slugs, author_name) in enumerate(ARTICLES):
            article, created = Article.objects.get_or_create(
                title=title,
                defaults={
                    'summary': 'Resumen de la noticia: ' + 'contenido de ejemplo para el portal, ' * 8,
                    'body': HTML_BODY if index == 5 else 'Primer párrafo de la noticia.\n\nSegundo párrafo con más detalles del suceso.',
                    'published_at': now - timedelta(days=index),
                    'author': authors[author_name],
                },
            )
            if created:
                article.featured_image.save(f'article_{index + 1}.png', make_image(COLORS[index], title[:40]))
                article.categories.set([categories[s] for s in slugs])
        self.stdout.write(self.style.SUCCESS('Datos de ejemplo cargados.'))
