from django.contrib import admin
from .models import Post
from .models import Comment  # importa de blog/models.py
from .models import Document  # importa de blog/models.py

# tablas de la BD a las que accederemos desde el panel de admin
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Document)
