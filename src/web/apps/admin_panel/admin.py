from django.contrib import admin


class AdminPanel(admin.AdminSite):
    site_header = 'Custom Admin Panel'
    site_title = 'Admin Panel'
    index_title = 'Welcome to Admin Panel'
    site_url = None
    enable_nav_sidebar = True


admin_panel = AdminPanel(name='admin_panel')
