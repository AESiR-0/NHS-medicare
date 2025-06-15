from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from core.models import NurseDocument
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Checks for documents that are expiring soon and sends notifications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days before expiry to send notification'
        )

    def handle(self, *args, **options):
        days = options['days']
        expiry_date = timezone.now().date() + timedelta(days=days)
        
        expiring_documents = NurseDocument.objects.filter(
            expiry_date__lte=expiry_date,
            expiry_date__gt=timezone.now().date()
        ).select_related('nurse', 'nurse__agency')

        for document in expiring_documents:
            # Send email to agency
            subject = f'Document Expiring Soon: {document.nurse.full_name}'
            message = f"""
            The following document for {document.nurse.full_name} is expiring soon:
            
            Document Type: {document.get_document_type_display()}
            Expiry Date: {document.expiry_date}
            
            Please ensure to upload a new document before the expiry date.
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [document.nurse.agency.contact_email],
                fail_silently=True,
            )
            
            self.stdout.write(
                self.style.WARNING(
                    f'Notification sent for expiring document: {document}'
                )
            ) 