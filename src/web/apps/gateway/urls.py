from django.urls import path, include
from django.contrib import admin

from apps.gateway.views import RequestDashboard, ExceptionDashboard, get_modal_content
from apps.gateway.ping import ping

urlpatterns = [
    path('api/ping/', ping, name='ping'),
   
    ## Request Viewer URLs
    path('api/request-viewer/', RequestDashboard.as_view(), name="request-viewer"),
    path('api/request-viewer/exceptions', ExceptionDashboard.as_view(), name="exception-viewer"),
    path('api/modal-content/', get_modal_content, name='modal-content'),
    
    ## Admin URLs
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
]
