from django.shortcuts import redirect


def group_required(group_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                groups = request.user.groups.values_list('name', flat=True)
                if group_name in groups:
                    return view_func(request, *args, **kwargs)

            return redirect('login_user')

        return _wrapped_view

    return decorator


admin_required = group_required('Admins')
caregiver_required = group_required('Caregivers')
patient_required = group_required('Patients')
