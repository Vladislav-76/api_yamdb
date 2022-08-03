from django.contrib import admin

from .models import User, Title, Review, Genre, Category, Title

admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Category)
