from django.contrib import messages
from django.shortcuts import redirect


def patient_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if 'Patients' in request.user.groups.values_list('name', flat=True):
                return view_func(request, *args, **kwargs)
            else:
                messages.success(request, 'Na tuto část webu nemáte přístup.')
                return redirect('login_user')
        else:
            messages.success(request, 'Pro přístup do aplikace se přihlašte')
            return redirect('login_user')

    return _wrapped_view
