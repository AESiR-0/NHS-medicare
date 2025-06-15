from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import NHSTrust, Hospital, Agency, TrustAgencyAccess, Nurse, NurseDocument, Shift, Booking
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial test data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating seed data...')

        # Create NHS Trust
        trust = NHSTrust.objects.create(
            name='NHS London Trust',
            website='https://www.nhs.uk',
            region='London',
            contact_email='contact@nhslondon.nhs.uk',
            contact_phone='02012345678'
        )

        # Create Admin User (if not exists)
        if not User.objects.filter(username='seed_admin').exists():
            admin_user = User.objects.create_superuser(
                username='seed_admin',
                email='seed_admin@example.com',
                password='admin123',
                role='admin'
            )
        else:
            admin_user = User.objects.get(username='seed_admin')

        # Create Hospital User and Hospital
        if not User.objects.filter(username='seed_hospital').exists():
            hospital_user = User.objects.create_user(
                username='seed_hospital',
                email='seed_hospital@example.com',
                password='hospital123',
                role='hospital'
            )
        else:
            hospital_user = User.objects.get(username='seed_hospital')

        hospital = Hospital.objects.create(
            trust=trust,
            user=hospital_user,
            name='St. Mary\'s Hospital',
            address='Praed Street, London W2 1NY',
            postcode='W2 1NY',
            phone='02033121234',
            emergency_contact='Emergency Department'
        )

        # Create Agency User and Agency
        if not User.objects.filter(username='seed_agency').exists():
            agency_user = User.objects.create_user(
                username='seed_agency',
                email='seed_agency@example.com',
                password='agency123',
                role='agency'
            )
        else:
            agency_user = User.objects.get(username='seed_agency')

        agency = Agency.objects.create(
            user=agency_user,
            name='Nursing Solutions Ltd',
            contact_email='contact@nursingsolutions.com',
            phone='02087654321',
            address='123 Business Street, London',
            registration_number='REG123456',
            vat_number='GB123456789'
        )

        # Create Trust-Agency Access
        TrustAgencyAccess.objects.create(
            trust=trust,
            agency=agency,
            approved=True,
            approved_by=admin_user
        )

        # Create Nurse
        nurse = Nurse.objects.create(
            agency=agency,
            full_name='Jane Smith',
            dob=timezone.now().date() - timedelta(days=365*30),  # 30 years old
            registration_number='NMC123456',
            specialty='General Nursing',
            is_approved=True,
            approved_by=admin_user
        )

        # Create Nurse Documents
        NurseDocument.objects.create(
            nurse=nurse,
            document_type='registration',
            file_url='nurse_documents/registration.pdf',
            expiry_date=timezone.now().date() + timedelta(days=365),
            verified=True,
            verified_by=admin_user
        )

        # Create Shifts
        for i in range(5):
            shift = Shift.objects.create(
                hospital=hospital,
                ward='Ward ' + str(i+1),
                specialty_required='General Nursing',
                po_number=f'PO{i+1}',
                shift_date=timezone.now().date() + timedelta(days=i),
                shift_time=timezone.now().time(),
                duration_hours=8.0,
                rate_per_hour=25.00
            )

            # Create Booking for some shifts
            if i < 2:
                Booking.objects.create(
                    shift=shift,
                    nurse=nurse,
                    agency=agency,
                    confirmed=True
                )

        self.stdout.write(self.style.SUCCESS('Successfully created seed data')) 