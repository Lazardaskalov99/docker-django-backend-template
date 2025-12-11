from django.urls import path

from apps.gateway.ping import ping
from apps.admin_panel.admin import admin_panel

urlpatterns = [
    path('api/ping/', ping, name='ping'),
    
    ## Admin URLs
    path('api/admin/', admin_panel.urls),
]
