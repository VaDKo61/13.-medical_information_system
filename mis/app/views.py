from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN

from .filters import ConsultationFilter
from .models import Consultation
from .serializers import ConsultationSerializer, ChangeStatusSerializer
from .permissions import ConsultationPermission


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = (Consultation.objects.
                select_related('doctor', 'patient').
                all().
                order_by('-created_at'))
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
        else:
            qs = qs.none()
        return qs.order_by('-created_at')

    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
        consultation = self.get_object()
        if request.user.role == 'patient':
            return Response(
                {'detail': 'Вы не можете менять статус консультации'},
                status=HTTP_403_FORBIDDEN
            )
        serializer = ChangeStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        consultation.status = serializer.validated_data['status']
        consultation.save()

        return Response(self.get_serializer(consultation).data)
