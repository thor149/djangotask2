from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
import uuid
from datetime import datetime, timedelta
import pytz
from django.utils import timezone

class Appointment(models.Model):
    doctor = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='booked_appointments')
    specialty = models.CharField(max_length=200, default='General')
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def save(self, *args, **kwargs):
        if self.doctor.account_user_type != 'doctor':
            raise ValueError("The assigned doctor must have an account_user_type of 'doctor'.")
        if self.patient.account_user_type != 'patient':
            raise ValueError("The patient must have an account_user_type of 'patient'.")

        start_datetime = datetime.combine(self.appointment_date, self.start_time)
        if timezone.is_naive(start_datetime):
            start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())
        
        end_datetime = start_datetime + timedelta(minutes=45)
        self.start_time = start_datetime.time()
        self.end_time = end_datetime.time()

        super(Appointment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.username} on {self.appointment_date} at {self.start_time}"

