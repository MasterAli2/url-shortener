from django.shortcuts import render, redirect
from django.http import HttpRequest

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.forms import SetPasswordForm,PasswordChangeForm
from . forms import UpdateProfileForm


@login_required
def account_view(request: HttpRequest):
    form_type = request.POST.get('form_type')
    
    password_dropdown = False
    if request.user.has_usable_password():
        password_form = PasswordChangeForm(request.user, request.POST or None)
    else:
        password_form = SetPasswordForm(request.user, request.POST or None)
    profile_form = UpdateProfileForm(request.POST or None, instance=request.user)

    if request.method == 'POST':
        if form_type == 'password':
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)
                return redirect(request.path)
            password_dropdown = True
        if form_type == 'profile' and profile_form.is_valid():
            profile_form.save()
            return redirect(request.path)
        if form_type == "delete":
            request.user.delete()
            return redirect('/')
        
    return render(request, 'account.html', {'password_form': password_form,
                                            'has_password':request.user.has_usable_password(),
                                            'has_discord': request.user.social_auth
                                                .filter(provider='discord').exists(),
                                            'profile_form':profile_form,
                                            'drop_pass':password_dropdown})

