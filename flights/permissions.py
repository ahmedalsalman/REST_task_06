from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta
from django.utils import timezone
class IsStaffOrBooker(BasePermission):
	message = "NO!"
	def has_object_permission(self, request, view, obj):
		if (request.user.is_staff or request.user == obj.user):
			return True
		return False



class IsMoreThanThreeDaysAway(BasePermission):
	message = "Too late!"
	def has_object_permission(self, request, view, obj):
#		start_date = datetime.today(), "%Y-%m-%d %H:%M"
#		end_date = datetime.datetime.strptime(self.request.data.get('date'), "%Y-%m-%d %H:%M"
#		d = abs((end_date-start_date).days)
		d = (obj.date - timezone.now().date()).days
		if (d > 3):
			return True
		return False
