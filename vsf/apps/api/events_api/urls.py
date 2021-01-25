from .                      import views
from django.contrib         import admin
from django.urls            import include, path, re_path

app_name = "events_api"

urlpatterns = [
    path(
        '', 
        views.ListEvents.as_view(), 
        name='list_events'
        ),

    path(
        '<int:id>', 
        views.EventDetail.as_view(), 
        name='event_detail'),

    path(
        'num-active', 
        views.EventActiveNumber.as_view(), 
        name='event_active_num'),

    path(
        'num-asn', 
        views.EventAsnNumber.as_view(), 
        name='event_asn_num'),

    path(
        'num-type', 
        views.EventTypeNumber.as_view(), 
        name='event_type_num'),
]