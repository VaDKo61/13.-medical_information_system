from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST

from .filters import ConsultationFilter
from .models import Consultation
from .serializers import ConsultationSerializer
from .permissions import ConsultationPermission


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.select_related('doctor', 'patient').all()
    serializer_class = ConsultationSerializer
    permission_classes = [IsAuthenticated, ConsultationPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConsultationFilter

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', None)
        qs = super().get_queryset()
        if role == 'doctor' and getattr(user, 'doctor_profile', None):
            return qs.filter(doctor=user.doctor_profile)
        if role == 'patient' and getattr(user, 'patient_profile', None):
            return qs.filter(patient=user.patient_profile)
        return qs

    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request):
        consultation = self.get_object()
        if request.user.role == 'patient':
            return Response(
                {'detail': 'Вы не можете менять статус консультации'},
                status=HTTP_403_FORBIDDEN
            )
        new_status = request.data.get('status')
        if new_status not in dict(Consultation.STATUS_CHOICES):
            return Response(
                {'detail': 'Invalid status'},
                status=HTTP_400_BAD_REQUEST)
        consultation.status = new_status
        consultation.save()
        return Response(self.get_serializer(consultation).data)
