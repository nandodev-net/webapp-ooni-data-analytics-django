from django.urls import include
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

app_name = 'api'

urlpatterns = [
    path(
        'ooni_fp/',
        include('apps.api.fp_tables_api.urls', namespace='fp_tables'),
        ),

    path(
        'public_stats/',
        include('apps.api.public_stats_api.urls', namespace='public_stats'),
        ),

    path(
        'asns/',
        include('apps.api.asns_api.urls', namespace='asns'),
        ),

    path(
        'cases/',
        include('apps.api.cases_api.urls', namespace='cases'),
        ),

    path(
        'events/',
        include('apps.api.events_api.urls', namespace='events'),
        ),       

    path(
        'measurements/',
        include('apps.api.measurements_api.urls', namespace='measurements'),
        ), 

        path(
        'api-token-auth/', 
        obtain_auth_token, name='api_token_auth'),
]