from datetime import datetime
from babel.dates import format_date

from django.db.models import Q, F, ExpressionWrapper, BooleanField
from django.forms import modelformset_factory
from django.shortcuts import render, redirect

from home.decorators import caregiver_required
from patient.models import Patient, Activity
from home.forms import ObservationForm, PatientActivityForm
from home.views import delete_from_database


@caregiver_required
def index(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    context = {
        'first_name': first_name,
        'last_name': last_name
    }
    return render(request, 'index_caregiver.html', context)


@caregiver_required
def medical_cards(request):
    patients = Patient.objects.all().order_by('user__last_name')
    return render(request, 'medical_cards.html', {'patients': patients})


@caregiver_required
def patient_info(request, full_name_of_patient):
    first_name, last_name = full_name_of_patient.split('-')
    patient = Patient.objects.get(user__first_name=first_name, user__last_name=last_name)
    form = ObservationForm(request.POST or None, instance=patient)

    if form.is_valid():
        form.save()
        return redirect('patient_info', full_name_of_patient)

    context = {
        'patient': patient,
        'form': form
    }

    return render(request, 'patient_info.html', context)


@caregiver_required
def shift_schedule(request):
    now = datetime.now()
    caregiver = request.user.caregiver_profile
    context = {'caregiver': caregiver}

    shifts_to_display = caregiver.shift_set.annotate(
        is_overnight=ExpressionWrapper(
            Q(end__lt=F('start')),
            output_field=BooleanField()
        )
    ).filter(
        Q(date_of_shift__gt=now.date()) |
        (Q(date_of_shift=now.date()) & (Q(end__gt=now.time()) | Q(is_overnight=True)))
    ).order_by('date_of_shift', 'start')

    delete_from_database(caregiver.shift_set.filter(caregiver=caregiver), shifts_to_display)

    if shifts_to_display:
        context.update({'any_shifts': True})
        soonest_shift = shifts_to_display.first()
        shift_start = datetime.combine(soonest_shift.date_of_shift, soonest_shift.start)
        shift_end = datetime.combine(soonest_shift.date_of_shift, soonest_shift.end)

        # smeny dnes (probihaji nebo jeste budou)
        if shift_start <= now <= shift_end or soonest_shift.date_of_shift == now.date():
            context.update({
                'today': True,
                'shift_start': shift_start.time,
                'shift_end': shift_end.time
            })
            shifts_to_display = shifts_to_display[1:]

        # nadchazejici smeny
        if shifts_to_display:
            upcoming_shifts_info = []
            for upcoming_shift in shifts_to_display:
                upcoming_shifts_info.append({
                    'upcom_shift_date': format_date(upcoming_shift.date_of_shift, format='EEEE d. MMMM',
                                                    locale='cs_CZ'),
                    'upcom_shift_start': upcoming_shift.start,
                    'upcom_shift_end': upcoming_shift.end
                })

            context.update({'upcoming_shifts_info': upcoming_shifts_info})

    else:
        context.update({'any_shifts': False})

    return render(request, 'shift_schedule.html', context)


@caregiver_required
def patient_schedules(request):
    now = datetime.now()
    patients = Patient.objects.all().order_by('user__last_name')
    patients_info = []

    for patient in patients:
        todays_activities = []
        other_activities = []
        activities = patient.activity_set.filter(date__gte=now.date())
        delete_from_database(patient.activity_set.filter(patient=patient), activities)

        for activity in activities:
            if activity.date == now.date():
                todays_activities.append({'activity': activity})
            else:
                activity.date = format_date(activity.date, format='EEEE d. MMMM', locale='cs_CZ')
                other_activities.append({'activity': activity})

        patients_info.append({
            'patient': patient,
            'todays_activities': todays_activities,
            'other_activities': other_activities
        })

    context = {'patients_info': patients_info}

    return render(request, 'patient_schedules.html', context)


@caregiver_required
def edit_patient_schedules(request, pk):
    patient = Patient.objects.get(pk=pk)
    activities = Activity.objects.all().filter(patient=patient)

    formset_class = modelformset_factory(Activity, form=PatientActivityForm, extra=0, can_delete=True)
    formset = formset_class(request.POST or None, queryset=activities)
    for form, obj in zip(formset, activities):
        form.initial['date'] = obj.date.strftime('%Y-%m-%d')

    if formset.is_valid():
        for form in formset:
            if form.has_changed():
                activity = form.save(commit=False)
                activity.patient = patient
                activity.save()

        formset.save()
        return redirect('patient_schedules')

    context = {
        'patient': patient,
        'formset': formset
    }

    return render(request, 'edit_patient_schedules.html', context)


@caregiver_required
def manual(request):
    return render(request, 'manual.html')


@caregiver_required
def what_to_do(request):
    return render(request, 'what_to_do.html')


@caregiver_required
def free_time_activities(request):
    return render(request, 'free_time_activities.html')


@caregiver_required
def education(request):
    return render(request, 'education.html')
