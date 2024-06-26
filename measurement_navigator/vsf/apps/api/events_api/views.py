import json

import pytz
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response

from apps.main.asns.models import ASN
from apps.main.events.models import Event
from apps.main.measurements.submeasurements.models import *

from .serializers import (EventActiveNumberSerializer,
                          EventAsnNumberSerializer, EventDataSerializer,
                          EventDetailDataSerializer, EventDetailSerializer,
                          EventTypeNumberSerializer)

utc = pytz.UTC


class ListEvents(generics.GenericAPIView):
    """
    class created to provide response to endpoint listing
    all event instances in the database
    """

    serializer_class = EventDataSerializer
    queryset = Event.objects.all()

    def get(self, request):
        events = Event.objects.all()
        events_json = EventDataSerializer(events, many=True)
        return Response(events_json.data, status=status.HTTP_200_OK)


class EventDateDetail(generics.GenericAPIView):
    """
    class created to provide response to endpoint
    returning one event instance by id
    """

    serializer_class = EventDetailDataSerializer

    def get_object(self, id):
        try:
            return Event.objects.get(id=id)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, id, start_date, end_date):
        event = self.get_object(id)
        subms = ["dns", "tcp", "http"]
        measurements = []

        for subm in subms:
            ms = Measurement.objects.raw(
                f"SELECT DISTINCT measurements_measurement.* \
                FROM measurements_measurement   JOIN submeasurements_{subm} subm ON subm.measurement_id=measurements_measurement.id \
                                                JOIN measurements_rawmeasurement rms ON rms.id = measurements_measurement.raw_measurement_id\
                WHERE subm.event_id=%s AND rms.measurement_start_time >= %s AND rms.measurement_start_time <= %s",
                [id, start_date, end_date],
            )

            measurements += list(ms)

        _event = {"event": event, "measurements": measurements}
        event_json = EventDetailSerializer(_event)
        return Response(event_json.data, status=status.HTTP_200_OK)


class EventDetail(generics.GenericAPIView):
    """
    class created to provide response to endpoint
    returning one event instance by id
    """

    serializer_class = EventDetailDataSerializer

    def get_object(self, id):
        try:
            return Event.objects.get(id=id)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, id):
        event = self.get_object(id)

        subms = ["dns", "tcp", "http"]
        measurements = []

        for subm in subms:
            ms = Measurement.objects.raw(
                f"SELECT DISTINCT measurements_measurement.* \
                FROM measurements_measurement   JOIN submeasurements_{subm} subm ON subm.measurement_id=measurements_measurement.id \
                                                JOIN measurements_rawmeasurement rms ON rms.id = measurements_measurement.raw_measurement_id\
                WHERE subm.event_id=%s",
                [id],
            )

            measurements += list(ms)

        _event = {"event": event, "measurements": measurements}
        event_json = EventDetailSerializer(_event)
        return Response(event_json.data, status=status.HTTP_200_OK)


class EventPartialDetail(generics.GenericAPIView):
    """
    class created to provide response to endpoint
    returning one event instance by id
    """

    serializer_class = EventDetailDataSerializer

    def get_object(self, id):
        try:
            return Event.objects.get(id=id)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, id):
        event = self.get_object(id)
        event_json = EventDetailDataSerializer(event)
        return Response(event_json.data, status=status.HTTP_200_OK)


class ListEventsByASN(generics.GenericAPIView):
    """
    class created to provide response to endpoint listing
    all event instances by ASN
    """

    serializer_class = EventDataSerializer

    def get(self, request, asn):
        events = Event.objects.filter(asn__asn=asn)
        events_json = EventDataSerializer(events, many=True)
        return Response(events_json.data, status=status.HTTP_200_OK)


class ListEventsByType(generics.GenericAPIView):
    """
    class created to provide response to endpoint listing
    all event instances by Type
    """

    serializer_class = EventDataSerializer

    def get(self, request, type):
        events = Event.objects.filter(issue_type=type)
        events_json = EventDataSerializer(events, many=True)
        return Response(events_json.data, status=status.HTTP_200_OK)


class EventActiveNumber(generics.GenericAPIView):
    """
    class created to provide response to endpoint
    returning total number of active events
    """

    queryset = Event.objects.all()

    def get(self, request):
        total_events = Event.objects.count()
        active_events = Event.objects.filter(end_date=None).count()

        events_json = {
            "total_events": total_events,
            "active_events": active_events,
            "inactive_events": total_events - active_events,
        }
        events_json = EventActiveNumberSerializer(events_json)

        return Response(events_json.data, status=status.HTTP_200_OK)


class EventAsnNumber(generics.GenericAPIView):
    queryset = Event.objects.all()

    def get(self, request):
        total_events = Event.objects.count()
        asns = ASN.objects.all()
        event_asn = {}

        for asn in asns:
            event_total = Event.objects.filter(asn=asn).count()
            event_activ = Event.objects.filter(asn=asn, end_date=None).count()

            event_asn[asn.asn] = {
                "name": asn.name,
                "total_events": event_total,
                "active_events": event_activ,
                "inactive_events": event_total - event_activ,
            }

        print(event_asn)
        event_json = {"total_events": total_events, "data": json.dumps(event_asn)}
        events_json = EventAsnNumberSerializer(event_json)

        return Response(events_json.data, status=status.HTTP_200_OK)


class EventTypeNumber(generics.GenericAPIView):
    queryset = Event.objects.all()

    def get(self, request):
        total_events = Event.objects.count()

        http_total = Event.objects.filter(issue_type="http").count()
        http_active = Event.objects.filter(issue_type="http", end_date=None).count()

        dns_total = Event.objects.filter(issue_type="dns").count()
        dns_active = Event.objects.filter(issue_type="dns", end_date=None).count()

        tcp_total = Event.objects.filter(issue_type="tcp").count()
        tcp_active = Event.objects.filter(issue_type="tcp").count()

        event_type = {
            "http": {
                "total_events": http_total,
                "active_events": http_active,
                "inactive_events": http_total - http_active,
            },
            "dns": {
                "total_events": dns_total,
                "active_events": dns_active,
                "inactive_events": dns_total - dns_active,
            },
            "tcp": {
                "total_events": tcp_total,
                "active_events": tcp_active,
                "inactive_events": tcp_total - tcp_active,
            },
        }

        event_json = {"total_events": total_events, "data": json.dumps(event_type)}
        events_json = EventTypeNumberSerializer(event_json)

        return Response(events_json.data, status=status.HTTP_200_OK)
