from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        AGENCY = 'agency', _('Agency')
        HOSPITAL = 'hospital', _('Hospital')
    
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.HOSPITAL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.email} ({self.role})"

    def increment_failed_login(self):
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        if self.failed_login_attempts >= 5:
            self.is_active = False
        self.save()

    def reset_failed_login(self):
        self.failed_login_attempts = 0
        self.last_failed_login = None
        self.save()

class NHSTrust(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    region = models.CharField(max_length=100, null=True, blank=True, default="")
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    trust = models.ForeignKey(NHSTrust, on_delete=models.CASCADE, related_name='hospitals')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hospital')
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True, default="")
    postcode = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Agency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agency')
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(null=True, blank=True, default="")
    phone = models.CharField(max_length=20, null=True, blank=True, default="")
    address = models.TextField(null=True, blank=True)
    registration_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    vat_number = models.CharField(max_length=50, blank=True)
    approved_trusts = models.ManyToManyField(NHSTrust, through='TrustAgencyAccess')
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TrustAgencyAccess(models.Model):
    trust = models.ForeignKey(NHSTrust, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_accesses')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('trust', 'agency')

    def save(self, *args, **kwargs):
        if self.approved and not self.approved_at:
            self.approved_at = timezone.now()
        super().save(*args, **kwargs)

class Nurse(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='nurses')
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    registration_number = models.CharField(max_length=50, unique=True, null=True, blank=True, default="")
    specialty = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_nurses')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.full_name

    def clean(self):
        if self.dob and self.dob > timezone.now().date():
            raise ValidationError({'dob': 'Date of birth cannot be in the future'})

    def save(self, *args, **kwargs):
        if self.is_approved and not self.approved_at:
            self.approved_at = timezone.now()
        super().save(*args, **kwargs)

class NurseDocument(models.Model):
    DOCUMENT_TYPES = [
        ('id', 'ID Proof'),
        ('qualification', 'Qualification'),
        ('registration', 'Registration'),
        ('dbs', 'DBS Check'),
        ('insurance', 'Insurance'),
        ('other', 'Other'),
    ]

    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=100, choices=DOCUMENT_TYPES)
    file_url = models.FileField(upload_to='nurse_documents/')
    expiry_date = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='verified_documents')
    verified_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nurse.full_name} - {self.document_type}"

    def clean(self):
        if self.expiry_date and self.expiry_date < timezone.now().date():
            raise ValidationError({'expiry_date': 'Expiry date cannot be in the past'})

class Shift(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', _('Open')
        BOOKED = 'booked', _('Booked')
        COMPLETED = 'completed', _('Completed')
        CANCELLED = 'cancelled', _('Cancelled')

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='shifts')
    ward = models.CharField(max_length=100, null=True, blank=True, default="")
    specialty_required = models.CharField(max_length=100, null=True, blank=True, default="")
    po_number = models.CharField(max_length=50, null=True, blank=True, default="")
    shift_date = models.DateField()
    shift_time = models.TimeField()
    duration_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    rate_per_hour = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.hospital.name} - {self.shift_date} {self.shift_time}"

    def clean(self):
        if self.shift_date and self.shift_date < timezone.now().date():
            raise ValidationError({'shift_date': 'Shift date cannot be in the past'})

class Booking(models.Model):
    shift = models.OneToOneField(Shift, on_delete=models.CASCADE, related_name='booking')
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name='bookings')
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nurse.full_name} - {self.shift}"

    def save(self, *args, **kwargs):
        if self.confirmed and not self.confirmed_at:
            self.confirmed_at = timezone.now()
        if self.cancelled and not self.cancelled_at:
            self.cancelled_at = timezone.now()
        super().save(*args, **kwargs)
