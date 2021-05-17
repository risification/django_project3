from django.utils.datetime_safe import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from documentapp.models import *
from django.utils import timezone


class DocumentSerializers(serializers.ModelSerializer):
    check_date = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Document
        fields = ['id', 'title', 'text', 'file', 'date_created',
                  'date_expired', 'status', 'document_root', 'check_date', 'user']

    def get_check_date(self, obj):
        date_expired = obj.date_expired
        date_now = datetime.date(timezone.now())
        if date_now >= date_expired:
            obj.status = 'dead'
            obj.save()
        return 1

    def create(self, validated_data):
        user = validated_data.pop('user')
        group = user.groups.all()[0].name
        doc_root = validated_data['document_root']
        if group == 'general' and doc_root in ['public', 'private', 'secret']:
            document = Document.objects.create(**validated_data)
        elif group == 'president':
            document = Document.objects.create(**validated_data)
        else:
            raise ValidationError("You have no permissions!")
        return document
