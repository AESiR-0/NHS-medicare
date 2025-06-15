from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, NHSTrust, Hospital, Agency, TrustAgencyAccess,
    Nurse, NurseDocument, Shift, Booking
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)

@admin.register(NHSTrust)
class NHSTrustAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'trust', 'user')
    list_filter = ('trust',)
    search_fields = ('name', 'address')

@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'contact_email', 'phone')
    search_fields = ('name', 'contact_email')

@admin.register(TrustAgencyAccess)
class TrustAgencyAccessAdmin(admin.ModelAdmin):
    list_display = ('trust', 'agency', 'approved', 'created_at')
    list_filter = ('approved',)
    search_fields = ('trust__name', 'agency__name')

@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'agency', 'registration_number', 'specialty', 'is_approved')
    list_filter = ('is_approved', 'specialty', 'agency')
    search_fields = ('full_name', 'registration_number')

@admin.register(NurseDocument)
class NurseDocumentAdmin(admin.ModelAdmin):
    list_display = ('nurse', 'document_type', 'expiry_date', 'uploaded_at')
    list_filter = ('document_type',)
    search_fields = ('nurse__full_name', 'document_type')

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'ward', 'specialty_required', 'shift_date', 'shift_time', 'status')
    list_filter = ('status', 'specialty_required', 'hospital')
    search_fields = ('ward', 'po_number')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('shift', 'nurse', 'agency', 'booked_at')
    list_filter = ('agency',)
    search_fields = ('nurse__full_name', 'shift__po_number')
