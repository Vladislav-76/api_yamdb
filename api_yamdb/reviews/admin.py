from django.contrib import admin
from users.models import User
from .models import (Genre, Category, Title, TitleGenre,
                     Review, Comment)

admin.site.register([User, Genre, Category, Title, TitleGenre,
                    Review, Comment])
