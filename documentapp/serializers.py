from django.utils.datetime_safe import datetime
from rest_framework import serializers
from documentapp.models import *
from django.utils import timezone


class DocumentSerializers(serializers.ModelSerializer):
    check_date = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ['id', 'title', 'text', 'file', 'date_created',
                  'date_expired', 'status', 'document_root', 'check_date']

    def get_check_date(self, obj):
        date_expired = obj.date_expired
        date_now = datetime.date(timezone.now())
        if date_now >= date_expired:
            obj.status = 'dead'
            obj.save()
        return 1
