from rest_framework.permissions import BasePermission, SAFE_METHODS


class ConsultationPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        role = getattr(user, 'role', None)

        if (
                role == 'admin'
                or getattr(user, 'is_staff', None)
                or getattr(user, 'is_superuser', None)
        ):
            return True
        if role == 'doctor' and getattr(request.user, 'doctor_profile', None):
            return (getattr(obj, 'doctor_id', None) ==
                    getattr(user.doctor_profile, 'id', None))
        if role == 'patient' and getattr(user, 'patient_profile', None):
            return (getattr(obj, 'patient_id', None) ==
                    getattr(user.patient_profile, 'id', None))
        return False

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(getattr(request.user, 'is_authenticated', False))
