from django.contrib import admin
from django.urls import path
from .views import custom_admin_view, RequestDashboard, get_modal_content, clear_logs, get_django_logs


class AdminPanel(admin.AdminSite):
    site_header = 'Custom Admin Panel'
    site_title = 'Admin Panel'
    index_title = 'Welcome to Admin Panel'
    site_url = None
    enable_nav_sidebar = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('custom/', self.admin_view(custom_admin_view), name='custom'),
            path('request-viewer/', self.admin_view(RequestDashboard.as_view()), name='request-viewer'),
            path('modal-content/', self.admin_view(get_modal_content), name='modal-content'),
            path('clear-logs/', self.admin_view(clear_logs), name='clear-logs'),
            path('django-logs/', self.admin_view(get_django_logs), name='django-logs'),
        ]
        return custom_urls + urls


admin_panel = AdminPanel(name='admin_panel')
