from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import NHSTrust, Hospital, Agency, TrustAgencyAccess, Nurse, Shift
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create admin user
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        self.stdout.write('Created admin user')

        # Create NHS Trusts
        trust1 = NHSTrust.objects.create(
            name='London NHS Trust',
            website='https://london.nhs.uk'
        )
        trust2 = NHSTrust.objects.create(
            name='Manchester NHS Trust',
            website='https://manchester.nhs.uk'
        )
        self.stdout.write('Created NHS Trusts')

        # Create Hospital users and hospitals
        hospital1_user = User.objects.create_user(
            username='hospital1',
            email='hospital1@example.com',
            password='hospital123',
            role='hospital'
        )
        hospital1 = Hospital.objects.create(
            trust=trust1,
            user=hospital1_user,
            name='St. Thomas Hospital',
            address='Westminster Bridge Rd, London SE1 7EH'
        )

        hospital2_user = User.objects.create_user(
            username='hospital2',
            email='hospital2@example.com',
            password='hospital123',
            role='hospital'
        )
        hospital2 = Hospital.objects.create(
            trust=trust2,
            user=hospital2_user,
            name='Manchester Royal Infirmary',
            address='Oxford Rd, Manchester M13 9WL'
        )
        self.stdout.write('Created Hospitals')

        # Create Agency users and agencies
        agency1_user = User.objects.create_user(
            username='agency1',
            email='agency1@example.com',
            password='agency123',
            role='agency'
        )
        agency1 = Agency.objects.create(
            user=agency1_user,
            name='London Nursing Agency',
            contact_email='contact@londonnursing.com',
            phone='02012345678'
        )

        agency2_user = User.objects.create_user(
            username='agency2',
            email='agency2@example.com',
            password='agency123',
            role='agency'
        )
        agency2 = Agency.objects.create(
            user=agency2_user,
            name='Manchester Nursing Agency',
            contact_email='contact@manchesternursing.com',
            phone='01612345678'
        )
        self.stdout.write('Created Agencies')

        # Create Trust-Agency access
        TrustAgencyAccess.objects.create(
            trust=trust1,
            agency=agency1,
            approved=True
        )
        TrustAgencyAccess.objects.create(
            trust=trust2,
            agency=agency2,
            approved=True
        )
        self.stdout.write('Created Trust-Agency access')

        # Create Nurses
        nurse1 = Nurse.objects.create(
            agency=agency1,
            full_name='John Smith',
            dob=datetime(1985, 5, 15),
            registration_number='NMC123456',
            specialty='ICU',
            is_approved=True
        )
        nurse2 = Nurse.objects.create(
            agency=agency1,
            full_name='Sarah Johnson',
            dob=datetime(1990, 8, 22),
            registration_number='NMC234567',
            specialty='A&E',
            is_approved=True
        )
        nurse3 = Nurse.objects.create(
            agency=agency2,
            full_name='Michael Brown',
            dob=datetime(1988, 3, 10),
            registration_number='NMC345678',
            specialty='Surgery',
            is_approved=True
        )
        self.stdout.write('Created Nurses')

        # Create Shifts
        today = datetime.now().date()
        Shift.objects.create(
            hospital=hospital1,
            ward='ICU',
            specialty_required='ICU',
            po_number='PO001',
            shift_date=today + timedelta(days=1),
            shift_time=datetime.strptime('08:00', '%H:%M').time(),
            status='open'
        )
        Shift.objects.create(
            hospital=hospital2,
            ward='A&E',
            specialty_required='A&E',
            po_number='PO002',
            shift_date=today + timedelta(days=2),
            shift_time=datetime.strptime('16:00', '%H:%M').time(),
            status='open'
        )
        self.stdout.write('Created Shifts')

        self.stdout.write(self.style.SUCCESS('Successfully seeded data')) 