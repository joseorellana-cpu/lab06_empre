# Laboratorio 06 — Motor de plantillas con Django

**Curso:** Desarrollo de Aplicaciones Empresariales (4-C24-A)
**Proyecto:** `config` · **Aplicación:** `news`

## 1. Puesta en marcha

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_news        # 6 noticias, 3 categorías, 2 autores
python manage.py createsuperuser  # ya existe el usuario demo: admin / admin12345
python manage.py runserver
```

- Portal: http://127.0.0.1:8000/
- Administrador: http://127.0.0.1:8000/admin/ → `admin` / `admin12345`
- Pruebas: `python manage.py test` → **7 pruebas OK**

## 2. Estructura de plantillas (orden y propósito)

```
templates/
└── base.html                     Cabecera, menú, bloques title/content/sidebar y pie
news/templates/news/
├── home.html                     Portada: for + empty + include de la tarjeta
├── article_detail.html           Detalle: imagen, autor, categorías; sidebar con block.super
├── category_list.html            Listado por categoría: reutiliza la misma tarjeta
└── partials/
    └── _article_card.html        Fragmento único de tarjeta (imagen, fecha, truncado, etiquetas)
```

| Plantilla | Qué hace | Qué NO hace |
|---|---|---|
| `base.html` | Estructura común y navegación | No conoce artículos concretos |
| `home.html` | Recorre `articles` y muestra vacío si no hay | No filtra ni ordena (lo hace la vista) |
| `category_list.html` | Recorre los artículos de una categoría | No repite el marcado de la tarjeta |
| `article_detail.html` | Muestra un artículo y su autor | No calcula nada |
| `_article_card.html` | Formatea fecha (`date`), resumen (`truncatewords`) y etiquetas | No decide qué artículos se ven |

Las vistas (`news/views.py`) solo consultan el modelo; la plantilla recorre, condiciona y formatea.

## 3. Auto-escaping (paso 12)

La noticia nº 6 guarda HTML **en el cuerpo** (`news/management/commands/seed_news.py`, `HTML_BODY`):

```
Este párrafo contiene <b>negrita</b> y un <script>alert(1)</script> guardados tal cual.
```

Comprobación real con el cliente de Django:

```
status detail: 200
escaped body present: True      -> la página contiene &lt;b&gt;negrita&lt;/b&gt;
raw script present: False       -> la página NO contiene <script>alert(1)</script>
```

**Qué muestra la página:** el texto literal de las etiquetas; no pone negrita ni abre el diálogo.
**Por qué:** Django escapa por defecto toda variable (`<` → `&lt;`, `>` → `&gt;`), lo que evita XSS.
Solo se desactivaría con `|safe` o `{% autoescape off %}`, que aquí no se usan. El test
`news/tests.py::test_html_in_body_is_escaped` lo fija para que no se rompa.

## 4. Gestión desde el administrador

| Modelo | `list_display` | `list_filter` | `search_fields` | Extra |
|---|---|---|---|---|
| Author | name, email | — | name, email | — |
| Category | name, slug | — | name | slug automático |
| Article | title, author, published_at | categories, author | title, summary, body | `date_hierarchy`, `filter_horizontal` |

Todo el contenido del portal (títulos, resúmenes, cuerpos, imágenes, autores y categorías) sale de
la base de datos: se edita en `/admin/` y aparece en el sitio al recargar, sin tocar código.
Datos entregados: 6 noticias, 3 categorías, 2 autores, 6 imágenes en `media/articles/`.

## 5. Mapa con la rúbrica

| Criterio | Dónde se demuestra |
|---|---|
| 1. Herencia y fragmentos (5) | `base.html` + 3 plantillas que extienden + `_article_card.html` incluido 2 veces |
| 2. Variables, control y filtros (5) | `for`/`empty`/`if`, `date`, `truncatewords`, `linebreaks`, `default` |
| 3. Contenido desde el admin (5) | Admin personalizado + BD con superusuario `admin` |
| 4. Repositorio y observaciones (5) | Este documento + `README.md` + árbol de plantillas |

## 6. Observaciones y decisiones

1. **URLs siempre por nombre:** `news:home`, `news:detail`, `news:category`; ningún enlace está escrito a mano.
2. **Sidebar global:** `news/context_processors.py` entrega las categorías a todas las plantillas, sin repetir la consulta en cada vista.
3. **Sin N+1:** las vistas usan `select_related('author')` y `prefetch_related('categories')`.
4. **Imagen opcional:** si un artículo no tiene imagen destacada, la tarjeta usa `static/img/placeholder.png`.
5. **`DEFAULT_AUTO_FIELD = BigAutoField`** fijado en `settings.py` para que coincida con la migración (elimina el warning W042).
6. **Pruebas:** 7 casos cubren portada, vacío, detalle, categoría, escapado, 404 y hoja de estilos.
