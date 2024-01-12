from django.contrib import messages
from django.shortcuts import redirect


def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and 'Admins' in request.user.groups.values_list('name', flat=True):
            return view_func(request, *args, **kwargs)
        else:
            messages.success(request, 'Pro přístup do aplikace se přihlašte')
            return redirect('login_user')

    return _wrapped_view
