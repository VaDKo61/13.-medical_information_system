from rest_framework import serializers

from .models import *


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    clinics = ClinicSerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        exclude = ('user',)


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ('user',)


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate(self, data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        role = getattr(user, 'role', None)
        if user and role == 'patient':
            if 'patient' in data and data['patient'] != user:
                raise serializers.ValidationError('Пациент может создавать только свои записи.')
        if user and role == 'doctor':
            if 'doctor' in data and data['doctor'] != user:
                raise serializers.ValidationError('Доктор может создавать только свои записи.')
        return data
