from django.shortcuts import redirect


# Univerzální funkce, která uživatelovi bez konkrétní skupiny zakáže přístup na určitou část webu
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


# Inicializace funkcí, které kontrolují skupiny pro administrátory, opatrovníky a klienty
# Jsou využity ve views.py u většiny funkcí, jejíž přístup by měl být omezen
admin_required = group_required('Admins')
caregiver_required = group_required('Caregivers')
patient_required = group_required('Patients')
