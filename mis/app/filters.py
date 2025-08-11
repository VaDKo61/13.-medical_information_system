import django_filters

from .models import Consultation


class ConsultationFilter(django_filters.FilterSet):
    doctor_name = django_filters.CharFilter(method='filter_doctor_name')
    patient_name = django_filters.CharFilter(method='filter_patient_name')
    name = django_filters.CharFilter(method='filter_name')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    ordering = django_filters.OrderingFilter(
        fields=('created_at',),
        field_labels={
            'created_at': 'Дата создания',
        }
    )

    class Meta:
        model = Consultation
        fields = ['doctor_name', 'patient_name', 'name', 'status']

    def filter_doctor_name(self, queryset, name, value):
        return queryset.filter(
            doctor__first_name__icontains=value
        ) | queryset.filter(
            doctor__last_name__icontains=value
        ) | queryset.filter(
            doctor__surname__icontains=value
        )

    def filter_patient_name(self, queryset, name, value):
        return queryset.filter(
            patient__first_name__icontains=value
        ) | queryset.filter(
            patient__last_name__icontains=value
        ) | queryset.filter(
            patient__surname__icontains=value
        )

    def filter_name(self, queryset, name, value):
        doctor_qs = self.filter_doctor_name(queryset, value)
        patient_qs = self.filter_patient_name(queryset, value)
        return doctor_qs | patient_qs
