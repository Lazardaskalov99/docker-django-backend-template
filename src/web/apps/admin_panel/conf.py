from django.conf import settings

# Request viewer configs
REQUEST_VIEWER = getattr(settings, 'REQUEST_VIEWER', {})
LIVE_MONITORING = REQUEST_VIEWER.get('LIVE_MONITORING', True)
WHITELISTED_PATHS = REQUEST_VIEWER.get('WHITELISTED_PATH', [])
DATETIME_FORMAT = "%d %b %Y %H:%M:%S.%f"
