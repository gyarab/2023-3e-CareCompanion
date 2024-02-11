from django.contrib import messages
from django.shortcuts import redirect


def caregiver_required(view_func):
    def _wrapped_view(request, *args, **kwargs):

        if request.user.is_authenticated:
            groups = request.user.groups.values_list('name', flat=True)

            if 'Caregivers' in groups:
                return view_func(request, *args, **kwargs)
            elif 'Patients' in groups:
                messages.success(request, 'Na tuto část webu nemáte přístup.')
                return redirect('index_patient')
            elif 'Admins' in groups:
                messages.success(request, 'Na tuto část webu nemáte přístup.')
                return redirect('administration')
            else:
                messages.success(request, 'Obraťte se IT podporu.')
                return redirect('login_user')
        else:
            messages.success(request, 'Pro přístup do aplikace se přihlašte.')
            return redirect('login_user')

    return _wrapped_view
