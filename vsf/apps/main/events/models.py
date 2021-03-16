# WARNING: There's a lot of fields that require to be checked at some point,
# they're marked with a @TODO, please fix this configuration before launching 
# the production build

# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from datetime import datetime  

from django.db.models.deletion import SET_NULL

from apps.main.sites.models     import Domain 
from apps.main.asns.models      import ASN

class Event(models.Model):

    class IssueType(models.TextChoices):
        """
        	Every type of issue
        """
        TCP     =   'tcp'
        DNS     =   'dns'
        HTTP    =   'http'
        NDT     =   'ndt'
        NONE    =   'none'

    # Issue name
    identification = models.CharField(
        max_length=200
    )

    # Confirmed by an human
    confirmed = models.BooleanField(
        default = False,
        verbose_name = 'confirmed?'
    )

    # First Measurement date
    start_date = models.DateTimeField(
        auto_now_add=True, 
        blank=True
    )

    # Last measurement date
    end_date = models.DateTimeField(
        null=True, 
        blank=True
    )

    public_evidence = models.TextField(
        null=True, 
        blank=True
    )

    private_evidence = models.TextField(
        null=True, 
        blank=True
    )

    # Type of issue
    issue_type = models.CharField(
        max_length=10, 
        null=False, 
        choices=IssueType.choices, 
        default = IssueType.NONE
    )

    it_continues = models.BooleanField(
        default = True,
    )

    domain  = models.ForeignKey(
                            to=Domain,
                            null=True,
                            on_delete=SET_NULL
                            ) 

    asn = models.ForeignKey(
                            to=ASN,
                            null=True,
                            on_delete=SET_NULL
                            ) 

    # If true, then this event won't register new measurements
    closed = models.BooleanField(default=False) 

    def __str__(self):
        return u"%s" % self.identification
