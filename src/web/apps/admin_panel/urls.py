from django.urls import path
from .admin import admin_panel

urlpatterns = [
    path('', admin_panel.urls),
]
