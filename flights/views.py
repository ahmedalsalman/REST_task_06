from rest_framework.generics import (
ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView,
DestroyAPIView, CreateAPIView
)
from datetime import datetime, timedelta

from rest_framework.permissions import (
BasePermission, IsAuthenticated, IsAdminUser, AllowAny)

from .models import Flight, Booking

from .serializers import (
FlightSerializer, BookingSerializer,
BookingDetailsSerializer, UpdateBookingSerializer,
RegisterSerializer, AdminUpdateBookingSerializer
)

from .permissions import IsStaffOrBooker, IsMoreThanThreeDaysAway


class FlightsList(ListAPIView):
	queryset = Flight.objects.all()
	serializer_class = FlightSerializer


class BookingsList(ListAPIView):
	serializer_class = BookingSerializer
	permission_classes = [IsAuthenticated]
	def get_queryset(self):
		return Booking.objects.filter(user=self.request.user, date__gte=datetime.today())

class BookingDetails(RetrieveAPIView):
	queryset = Booking.objects.all()
	serializer_class = BookingDetailsSerializer
	permission_classes = [IsStaffOrBooker]

	lookup_field = 'id'
	lookup_url_kwarg = 'booking_id'


class UpdateBooking(RetrieveUpdateAPIView):
	queryset = Booking.objects.filter(date__gte=(datetime.today()))
	lookup_field = 'id'
	lookup_url_kwarg = 'booking_id'
	permission_classes = [IsStaffOrBooker, IsMoreThanThreeDaysAway]

	def get_serializer_class(self):
		if self.request.user.is_staff:
			return AdminUpdateBookingSerializer
		else:
			return UpdateBookingSerializer


class CancelBooking(DestroyAPIView):
	queryset = Booking.objects.all()
	permission_classes = [IsStaffOrBooker, IsMoreThanThreeDaysAway]
	lookup_field = 'id'
	lookup_url_kwarg = 'booking_id'
	



class BookFlight(CreateAPIView):
	serializer_class = AdminUpdateBookingSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Booking.objects.filter(user=self.request.user)
	def perform_create(self, serializer):
		serializer.save(user=self.request.user, flight_id=self.kwargs['flight_id'])


class Register(CreateAPIView):
	serializer_class = RegisterSerializer
