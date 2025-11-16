from django.contrib import admin
from django.urls import path, include
from button_app.views import index

urlpatterns = [
    path('admin/', admin.site.urls),  # Добавляем путь к админке
    path('', index, name='index'),
]