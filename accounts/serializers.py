from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .services import *
from .models import *


class RegisterSerializers(serializers.ModelSerializer):
    check_password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=(
        ("warrior", "warrior"),
        ("common", "common")
    ), write_only=True)
    full_name = serializers.CharField(write_only=True)
    image = serializers.ImageField(write_only=True)
    date_birth = serializers.DateField(write_only=True)
    gender = serializers.ChoiceField(choices=(
        ("M", "M"),
        ("F", "F")
    ), write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'check_password', 'full_name', 'date_birth', 'gender', 'image',
                  'user_type']

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        password = validated_data.pop('password')
        check_password = validated_data.pop('check_password')
        full_name = validated_data.pop('full_name')
        date_birth = validated_data.pop('date_birth')
        gender = validated_data.pop('gender')
        image = validated_data.pop('image')
        user = User.objects.create(**validated_data)
        if password != check_password:
            raise ValidationError("Passwords don't match")
        user.set_password(password)
        if user_type == 'warrior':
            user.is_active = False
            group = Group.objects.get(name='serjant')
            user.groups.add(group)
            mailing(user.username)
        user.save()
        Dossier.objects.create(full_name=full_name, date_birth=date_birth, gender=gender, image=image, user=user)
        return user


class CarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'mark', 'model', 'year', 'number', 'color', 'type', ]


class EducationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'start_date', 'end_date', 'school_name', 'major', ]


class WarcraftSerializers(serializers.ModelSerializer):
    class Meta:
        model = Warcraft
        fields = ['id', 'start_date', 'end_date', 'military_area',
                  'major', 'start_pose', 'end_pose', ]


class DossierSerializers(serializers.ModelSerializer):
    education = EducationSerializers(many=True)
    warcraft = WarcraftSerializers(many=True)
    car = CarSerializers(many=True)
    print(1)

    class Meta:
        model = Dossier
        fields = ['id', 'full_name', 'date_birth', 'image', 'gender', 'user',
                  'car', 'education', 'warcraft']

    def create(self, validated_data):
        car_data = validated_data.pop('car')
        print(car_data)
        education_data = validated_data.pop('education')
        print(education_data)
        warcraft_data = validated_data.pop('warcraft')
        print(warcraft_data)
        print(validated_data)
        dossier = Dossier.objects.create(**validated_data)
        for car in car_data:
            Car.objects.create(dossier=dossier, **car)
        for education in education_data:
            Education.objects.create(dossier=dossier, **education)
        for warcraft in warcraft_data:
            Warcraft.objects.create(dossier=dossier, **warcraft)
        return dossier
