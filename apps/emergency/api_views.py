from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Count, Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EmergencyRequest, RequestStatus
from .serializers import (
    EmergencyRequestSerializer,
    ReviewSerializer,
    SubmitEmergencySerializer,
    VerifyEmergencySerializer,
)
from .services import (
    add_public_review,
    buzz_request,
    create_emergency_request,
    is_emergency_operator,
    transition_request,
)


def _qs_for(user):
    qs = EmergencyRequest.objects.select_related("service", "requester").annotate(
        unread_buzz_count=Count("buzzes", filter=Q(buzzes__seen_by_operators=False))
    )
    if is_emergency_operator(user):
        return qs
    return qs.filter(requester=user)


class SubmitEmergencyRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubmitEmergencySerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            emergency = create_emergency_request(
                requester=request.user,
                service=data["service"],
                description=data["description"],
                saved_location=data.get("saved_location"),
                latitude=data.get("latitude"),
                longitude=data.get("longitude"),
            )
        except ValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        out = EmergencyRequestSerializer(emergency)
        return Response(out.data, status=status.HTTP_201_CREATED)


class SearchEmergencyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = _qs_for(request.user)
        q = request.query_params.get("q")
        status_param = request.query_params.get("status")
        service = request.query_params.get("service")
        if q:
            qs = qs.filter(
                Q(description__icontains=q) | Q(service__name__icontains=q)
            )
        if status_param:
            qs = qs.filter(status=status_param)
        if service:
            qs = qs.filter(service_id=service)
        return Response(EmergencyRequestSerializer(qs, many=True).data)


class VerifyEmergencyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        emergency = _qs_for(request.user).filter(pk=pk).first()
        if not emergency:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = VerifyEmergencySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            transition_request(
                emergency_request=emergency,
                actor=request.user,
                to_status=serializer.validated_data["to_status"],
                note=serializer.validated_data.get("note") or "",
            )
        except PermissionDenied as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        emergency.refresh_from_db()
        return Response(EmergencyRequestSerializer(emergency).data)


class CancelEmergencyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        emergency = _qs_for(request.user).filter(pk=pk).first()
        if not emergency:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            transition_request(
                emergency_request=emergency,
                actor=request.user,
                to_status=RequestStatus.CANCELLED,
                note=request.data.get("note") or "Cancelled via API",
            )
        except PermissionDenied as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        emergency.refresh_from_db()
        return Response(EmergencyRequestSerializer(emergency).data)


class BuzzEmergencyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        emergency = _qs_for(request.user).filter(pk=pk).first()
        if not emergency:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            buzz = buzz_request(emergency_request=emergency, user=request.user)
        except PermissionDenied as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"id": buzz.id, "created_at": buzz.created_at},
            status=status.HTTP_201_CREATED,
        )


class ReviewEmergencyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        emergency = _qs_for(request.user).filter(pk=pk).first()
        if not emergency:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            add_public_review(
                emergency_request=emergency,
                user=request.user,
                comment=serializer.validated_data["review_comment"],
                rating=serializer.validated_data.get("review_rating"),
            )
        except PermissionDenied as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as exc:
            return Response({"detail": exc.messages}, status=status.HTTP_400_BAD_REQUEST)
        emergency.refresh_from_db()
        return Response(EmergencyRequestSerializer(emergency).data)
