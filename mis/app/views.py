from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Consultation
from .serializers import ConsultationSerializer
from .permissions import ConsultationPermission


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.select_related('doctor', 'patient').all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated, ConsultationPermission]

    # filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    # search_fields = ['doctor__last_name', 'doctor__first_name', 'patient__last_name', 'patient__first_name']
    # ordering_fields = ['created_at']
    # filterset_fields = ['status']

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        qs = super().get_queryset()
        if role == 'doctor' and getattr(user, 'doctor_profile', None):
            return qs.filter(doctor=user.doctor_profile)
        if role == 'patient' and getattr(user, 'patient_profile', None):
            return qs.filter(patient=user.patient_profile)
        return qs
