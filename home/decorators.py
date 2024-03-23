from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            groups = request.user.groups.values_list('name', flat=True)
            if 'Admins' in groups:
                return view_func(request, *args, **kwargs)

        messages.success(request, 'Pro přístup do aplikace se přihlašte.')
        return redirect('login_user')
    return _wrapped_view
