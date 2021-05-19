from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .services import *
from .models import *


class CarSerializers(serializers.ModelSerializer):
    car_id = serializers.IntegerField(source='id', required=False)

    class Meta:
        model = Car
        fields = ['car_id', 'mark', 'model', 'year', 'number', 'color', 'type', ]


class EducationSerializers(serializers.ModelSerializer):
    education_id = serializers.IntegerField(source='id', required=False)

    class Meta:
        model = Education
        fields = ['education_id', 'start_date', 'end_date', 'school_name', 'major', ]


class WarcraftSerializers(serializers.ModelSerializer):
    warcraft_id = serializers.IntegerField(source='id', required=False)

    class Meta:
        model = Warcraft
        fields = ['warcraft_id', 'start_date', 'end_date', 'military_area',
                  'major', 'start_pose', 'end_pose', ]


class DossierSerializers(serializers.ModelSerializer):
    education = EducationSerializers(many=True)
    warcraft = WarcraftSerializers(many=True)
    car = CarSerializers(many=True)

    class Meta:
        model = Dossier
        fields = ['id', 'full_name', 'date_birth', 'image', 'gender', 'user',
                  'car', 'education', 'warcraft']

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        cars_data = validated_data.pop('car')
        education_data = validated_data.pop('education')
        warcraft_data = validated_data.pop('warcraft')
        ids_list_car = [car.id for car in instance.car.all()]
        current_ids_car = [car['id'] for car in cars_data]
        final_list_car = [car_id for car_id in ids_list_car if car_id not in current_ids_car]
        for car in cars_data:
            car_id = car['id']
            car_data = Car.objects.get(id=car_id)
            for delete_id in final_list_car:
                delete_car = Car.objects.get(id=delete_id)
                delete_car.delete()
            car_data.mark = car['mark']
            car_data.model = car['model']
            car_data.year = car['year']
            car_data.number = car['number']
            car_data.color = car['color']
            car_data.type = car['type']
            car_data.save()
        ids_list_education = [education.id for education in instance.education.all()]
        current_ids_education = [education['id'] for education in education_data]
        final_list_education = [education_id for education_id in ids_list_education if
                                education_id not in current_ids_education]
        for education in education_data:
            education_id = education['id']
            education_data = Education.objects.get(id=education_id)
            for delete_id in final_list_education:
                delete_car = Education.objects.get(id=delete_id)
                delete_car.delete()
            education_data.school_name = education['school_name']
            education_data.start_date = education['start_date']
            education_data.end_date = education['end_date']
            education_data.major = education['major']
            education_data.save()
        ids_list_warcraft = [warcraft.id for warcraft in instance.warcraft.all()]
        current_ids_warcraft = [warcraft['id'] for warcraft in warcraft_data]
        final_list_warcraft = [warcraft_id for warcraft_id in ids_list_warcraft if
                               warcraft_id not in current_ids_warcraft]
        for warcraft in warcraft_data:
            warcraft_id = warcraft['id']
            warcraft_data = Warcraft.objects.get(id=warcraft_id)
            for delete_id in final_list_warcraft:
                delete_warcraft = Warcraft.objecst.get(id=delete_id)
                delete_warcraft.delete()
            warcraft_data.military_area = warcraft['military_area']
            warcraft_data.start_date = warcraft['start_date']
            warcraft_data.end_date = warcraft['end_date']
            warcraft_data.major = warcraft['major']
            warcraft_data.start_pose = warcraft['start_pose']
            warcraft_data.end_pose = warcraft['end_pose']
            warcraft_data.save()
        instance.save()
        return instance

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
    dossier = DossierSerializers()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'check_password', 'full_name', 'date_birth', 'gender', 'image',
                  'user_type', 'dossier']

    @transaction.atomic
    def create(self, validated_data):
        user_type = validated_data.pop('user_type')
        password = validated_data.pop('password')
        check_password = validated_data.pop('check_password')
        full_name = validated_data.pop('full_name')
        date_birth = validated_data.pop('date_birth')
        gender = validated_data.pop('gender')
        image = validated_data.pop('image')
        if password != check_password:
            raise ValidationError("Passwords don't match")
        if not validate_password(password):
            raise ValidationError("пароль состоит только из цифр или из букв")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        if user_type == 'warrior':
            user.is_active = False
            group = Group.objects.get(name='serjant')
            user.groups.add(group)
            mailing(user.username)
        user.save()
        Dossier.objects.create(full_name=full_name, date_birth=date_birth, gender=gender, image=image, user=user)
        return user
