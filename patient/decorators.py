from django.contrib import messages
from django.shortcuts import redirect


def patient_required(view_func):
    def _wrapped_view(request, *args, **kwargs):

        if request.user.is_authenticated:
            groups = request.user.groups.values_list('name', flat=True)

            if 'Patients' in groups:
                return view_func(request, *args, **kwargs)
            elif 'Admins' in groups:
                messages.success(request, 'Na tuto část webu nemáte stupid.')
                return redirect('administration')
            elif 'Caregivers' in groups:
                messages.success(request, 'Na tuto část webu nemáte přístup.')
                return redirect('index_caregiver')
            else:
                messages.success(request, 'Obraťte se IT podporu.')
                return redirect('login_user')

        else:
            messages.success(request, 'Pro přístup do aplikace se přihlašte.')
            return redirect('login_user')

    return _wrapped_view
