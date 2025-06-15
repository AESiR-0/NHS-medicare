from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import (
    User, NHSTrust, Hospital, Agency, TrustAgencyAccess,
    Nurse, NurseDocument, Shift, Booking
)
from .forms import (
    NurseForm, NurseDocumentForm, ShiftForm, BookingForm
)

def is_admin(user):
    return user.role == 'admin'

def is_agency(user):
    return user.role == 'agency'

def is_hospital(user):
    return user.role == 'hospital'

@login_required
def dashboard(request):
    if request.user.role == 'admin':
        return render(request, 'core/admin_dashboard.html')
    elif request.user.role == 'agency':
        return render(request, 'core/agency_dashboard.html')
    elif request.user.role == 'hospital':
        return render(request, 'core/hospital_dashboard.html')
    return redirect('login')

# Agency Views
@login_required
@user_passes_test(is_agency)
def nurse_list(request):
    nurses = Nurse.objects.filter(agency=request.user.agency)
    return render(request, 'core/nurse_list.html', {'nurses': nurses})

@login_required
@user_passes_test(is_agency)
def nurse_create(request):
    if request.method == 'POST':
        form = NurseForm(request.POST)
        if form.is_valid():
            nurse = form.save(commit=False)
            nurse.agency = request.user.agency
            nurse.save()
            messages.success(request, 'Nurse added successfully.')
            return redirect('nurse_list')
    else:
        form = NurseForm()
    return render(request, 'core/nurse_form.html', {'form': form})

@login_required
@user_passes_test(is_agency)
def nurse_document_upload(request, nurse_id):
    nurse = get_object_or_404(Nurse, id=nurse_id, agency=request.user.agency)
    if request.method == 'POST':
        form = NurseDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.nurse = nurse
            document.save()
            messages.success(request, 'Document uploaded successfully.')
            return redirect('nurse_list')
    else:
        form = NurseDocumentForm()
    return render(request, 'core/document_form.html', {'form': form, 'nurse': nurse})

# Hospital Views
@login_required
@user_passes_test(is_hospital)
def shift_create(request):
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift = form.save(commit=False)
            shift.hospital = request.user.hospital
            shift.save()
            messages.success(request, 'Shift created successfully.')
            return redirect('shift_list')
    else:
        form = ShiftForm()
    return render(request, 'core/shift_form.html', {'form': form})

@login_required
@user_passes_test(is_hospital)
def shift_list(request):
    shifts = Shift.objects.filter(hospital=request.user.hospital)
    return render(request, 'core/shift_list.html', {'shifts': shifts})

# Agency Shift Views
@login_required
@user_passes_test(is_agency)
def available_shifts(request):
    approved_trusts = TrustAgencyAccess.objects.filter(
        agency=request.user.agency,
        approved=True
    ).values_list('trust', flat=True)
    
    shifts = Shift.objects.filter(
        hospital__trust__in=approved_trusts,
        status='open'
    )
    return render(request, 'core/available_shifts.html', {'shifts': shifts})

@login_required
@user_passes_test(is_agency)
def book_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id, status='open')
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.shift = shift
            booking.agency = request.user.agency
            booking.save()
            shift.status = 'booked'
            shift.save()
            messages.success(request, 'Shift booked successfully.')
            return redirect('available_shifts')
    else:
        form = BookingForm()
        form.fields['nurse'].queryset = Nurse.objects.filter(
            agency=request.user.agency,
            is_approved=True
        )
    return render(request, 'core/booking_form.html', {'form': form, 'shift': shift})

# Admin Views
@login_required
@user_passes_test(is_admin)
def approve_nurse(request, nurse_id):
    nurse = get_object_or_404(Nurse, id=nurse_id)
    nurse.is_approved = True
    nurse.save()
    messages.success(request, 'Nurse approved successfully.')
    return redirect('admin:nurse_changelist')

@login_required
@user_passes_test(is_admin)
def approve_agency_trust(request, access_id):
    access = get_object_or_404(TrustAgencyAccess, id=access_id)
    access.approved = True
    access.save()
    messages.success(request, 'Agency approved for trust successfully.')
    return redirect('admin:trustagencyaccess_changelist')
