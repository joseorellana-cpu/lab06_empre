# Laboratorio 06 — Motor de plantillas con Django

Portal de noticias (proyecto `config`, aplicación `news`).

## Cómo ejecutarlo

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_news      # 6 noticias, 3 categorías, 2 autores (opcional: el zip ya trae db.sqlite3)
python manage.py createsuperuser
python manage.py runserver
```

- Portal: http://127.0.0.1:8000/ — Administrador: http://127.0.0.1:8000/admin/
  (usuario demo incluido en `db.sqlite3`: **admin / admin12345**)
- Pruebas automáticas: `python manage.py test` (7 pruebas)

## Estructura y observaciones

| Ruta | Función |
|---|---|
| `templates/base.html` | Plantilla base: cabecera, menú, bloques `title`, `content`, `sidebar` y pie. |
| `news/templates/news/partials/_article_card.html` | Fragmento de tarjeta; se incluye con `{% include %}` desde portada y categoría (sin repetir marcado). |
| `news/templates/news/home.html` | Portada: `for` + `empty`, filtros `date` y `truncatewords`. |
| `news/templates/news/article_detail.html` | Detalle: imagen, autor, categorías; sobreescribe `sidebar` con `block.super`. |
| `news/templates/news/category_list.html` | Listado por categoría reutilizando la misma tarjeta. |
| `news/context_processors.py` | Entrega las categorías a la barra lateral de todas las páginas. |
| `news/urls.py` | Rutas con nombre: `news:home`, `news:detail`, `news:category`; los enlaces usan `{% url %}`. |
| `news/admin.py` | `list_display`, `list_filter` y `search_fields` en Author, Category y Article. |
| `news/management/commands/seed_news.py` | Carga de datos de ejemplo. |
| `static/` y `media/` | Estilos/imágenes del sitio y archivos subidos desde el admin. |

Las plantillas no contienen lógica de negocio: las vistas solo consultan el modelo y la plantilla recorre, condiciona y formatea.

## Prueba de escapado automático (paso 12)

La noticia nº 6 guarda en su **cuerpo** el texto `Este párrafo contiene <b>negrita</b> y un <script>alert(1)</script>`.
**Resultado:** la página muestra el texto literal de las etiquetas; no pone negrita ni ejecuta el script.
**Por qué:** Django escapa por defecto las variables (`<` → `&lt;`, `>` → `&gt;`), lo que evita ataques XSS. Solo se desactivaría con `|safe` o `{% autoescape off %}`, que aquí no se usan.

## Casos de prueba (`news/tests.py`)

1. La portada lista las noticias.
2. La portada sin noticias muestra el mensaje del bloque `empty`.
3. El detalle muestra el autor.
4. La categoría reutiliza la tarjeta y muestra sus noticias.
5. El HTML guardado en el cuerpo se escapa.
6. Un artículo inexistente devuelve 404.
7. La hoja de estilos se enlaza con `{% static %}`.

## Entregable

El detalle de la estructura de plantillas, el mapa con la rúbrica y las observaciones están en
[`ENTREGABLE_S06.md`](ENTREGABLE_S06.md).
