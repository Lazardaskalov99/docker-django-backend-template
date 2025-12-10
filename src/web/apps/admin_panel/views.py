from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import logging
from django.utils.decorators import method_decorator


from apps.admin_panel.models import Logger
from apps.gateway.utils import is_admin, filter_paths
from apps.admin_panel.conf import LIVE_MONITORING

# Create a custom log handler to store logs in memory
class MemoryLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.logs = []
        self.max_logs = 100
    
    def emit(self, record):
        log_entry = {
            'level': record.levelname,
            'message': self.format(record),
            'timestamp': self.formatter.formatTime(record) if self.formatter else '',
            'name': record.name
        }
        self.logs.append(log_entry)
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
    
    def get_logs(self):
        return self.logs

# Initialize the memory handler
memory_handler = MemoryLogHandler()
memory_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logging.getLogger('').addHandler(memory_handler)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class BaseView(generic.ListView):
    paginator = None
    page = 1
    middleware = None
    object_list = None

    def serialize_queryset(self):
        raise NotImplementedError('`serialize_queryset()` must be implemented.')

    def middleware_used(self):
        return self.middleware and self.middleware in settings.MIDDLEWARE

    def get_extra_data(self):
        self.page = self.request.GET.get('page', self.page)
        self.paginator = Paginator(self.serialize_queryset(), 50)

    def get_context_data(self, *args, **kwargs):
        context = super(BaseView, self).get_context_data(*args, **kwargs)
        self.get_extra_data()
        context['paginator'] = self.paginator
        context["is_connected"] = LIVE_MONITORING and self.middleware_used()
        context['object_list'] = self.paginator.page(self.page)
        return context


class RequestDashboard(BaseView):
    template_name = "request_viewer/request.html"
    model = Logger
    paginator = None
    middleware = "apps.gateway.middleware.RequestViewerMiddleware"

    def serialize_queryset(self):
        data = self.model.get_data()
        
        # Apply filtering first
        filter_by = getattr(self, 'filter_by', None)
        filter_value = getattr(self, 'filter_value', None)
        if filter_by and filter_value is not None:
            data = filter_paths(data, filter_by, filter_value)
        
        # Then apply sorting
        sort_by = getattr(self, 'sort_by', None)
        sort_order = getattr(self, 'sort_order', 'asc')
        
        if sort_by:
            reverse = sort_order == 'desc'
            try:
                data = sorted(data, key=lambda x: x.get(sort_by, ''), reverse=reverse)
            except:
                pass
        
        return data

    def post(self, request, *args, **kwargs):
        self.template_name = "request_viewer/fragments/request/table.html"
        self.filter_by = request.POST.get('filterBy')
        self.filter_value = request.POST.get('value')
        self.sort_by = request.POST.get('sortBy')
        self.sort_order = request.POST.get('sortOrder', 'asc')
        page = request.POST.get('page', 1)
        page = 1 if not page else page
        self.page = page
        self.get_extra_data()
        context = super(RequestDashboard, self).get_context_data(*args, **kwargs)
        return render(request, self.template_name, context)


@csrf_exempt
def get_modal_content(request):
    obj = json.loads(request.POST.get('obj'))
    entity = request.POST.get('entity', "request")
    return render(request, f'request_viewer/fragments/{entity}/modal_content.html', {'obj': obj})


@csrf_exempt
@user_passes_test(is_admin)
def clear_logs(request):
    if request.method == 'POST':
        Logger.objects.all().delete()
        return render(request, 'request_viewer/fragments/request/table.html', {'object_list': []})
    return render(request, 'request_viewer/fragments/request/table.html', {'object_list': []})


@csrf_exempt
@user_passes_test(is_admin)
def get_django_logs(request):
    logs = memory_handler.get_logs()
    return JsonResponse({'logs': logs[-50:]})  # Return last 50 logs


def custom_admin_view(request):
    return JsonResponse({'message': 'Custom admin panel endpoint'})

