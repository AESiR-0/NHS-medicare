from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

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

    def __str__(self):
        return f"{self.email} ({self.role})"

class NHSTrust(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    trust = models.ForeignKey(NHSTrust, on_delete=models.CASCADE, related_name='hospitals')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hospital')
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name

class Agency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agency')
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone = models.CharField(max_length=20)
    approved_trusts = models.ManyToManyField(NHSTrust, through='TrustAgencyAccess')

    def __str__(self):
        return self.name

class TrustAgencyAccess(models.Model):
    trust = models.ForeignKey(NHSTrust, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('trust', 'agency')

class Nurse(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='nurses')
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    registration_number = models.CharField(max_length=50, unique=True)
    specialty = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class NurseDocument(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=100)
    file_url = models.FileField(upload_to='nurse_documents/')
    expiry_date = models.DateField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nurse.full_name} - {self.document_type}"

class Shift(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', _('Open')
        BOOKED = 'booked', _('Booked')
        COMPLETED = 'completed', _('Completed')

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='shifts')
    ward = models.CharField(max_length=100)
    specialty_required = models.CharField(max_length=100)
    po_number = models.CharField(max_length=50)
    shift_date = models.DateField()
    shift_time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN
    )

    def __str__(self):
        return f"{self.hospital.name} - {self.shift_date} {self.shift_time}"

class Booking(models.Model):
    shift = models.OneToOneField(Shift, on_delete=models.CASCADE, related_name='booking')
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name='bookings')
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nurse.full_name} - {self.shift}"
