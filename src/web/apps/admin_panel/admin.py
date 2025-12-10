from django.contrib import admin
from django.urls import path
from .views import custom_admin_view, RequestDashboard, get_modal_content, clear_logs, get_django_logs


class AdminPanel(admin.AdminSite):
    site_header = 'Custom Admin Panel'
    site_title = 'Admin Panel'
    index_title = ''
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

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        for app in app_list:
            for model in app['models']:
                model['add_url'] = None
        return app_list


admin_panel = AdminPanel(name='admin_panel')

# Register models with the custom admin panel
from apps.gateway.models import Logger
from django.contrib.auth.models import User

@admin.register(Logger, site=admin_panel)
class LoggerAdmin(admin.ModelAdmin):
    list_display = ['id', 'path']
    search_fields = ['path']
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = self.model._meta.verbose_name_plural
        return super().changelist_view(request, extra_context=extra_context)

# Register default Django models
class UserAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Users'
        return super().changelist_view(request, extra_context=extra_context)

admin_panel.register(User, UserAdmin)

