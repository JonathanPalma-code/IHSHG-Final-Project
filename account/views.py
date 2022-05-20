from django.shortcuts import render, redirect
from django.contrib import messages  # import messages
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, UserPasswordResetForm
from .models import Profile
from django.contrib import messages

def index(request):
    registration_form = UserRegistrationForm() 
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():

            # Create a new user object but avoid saving it yet
            new_user = registration_form.save(commit=False)

            # Set the chosen password
            new_user.set_password(registration_form.cleaned_data['password'])

            # Save the user object
            new_user.save()
            Profile.objects.create(user=new_user)

            return render(request, 'account/register_done.html', {
                'new_user': new_user
            })
    else:
        registration_form = UserRegistrationForm()
    return render(request, 'account/index.html', {
        'registration_form': registration_form,
        'section': 'dashboard'
        })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                        data=request.POST,
                                        files=request.FILES)
                                        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
        else:
            messages.error(request, 'Error updating your profile.')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def password_reset_view(request):
	if request.method == "POST":
		password_reset_form = UserPasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "registration/password_reset_email.html"
					c = {
                        "user": user,
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'noreply_ihshg@outlook.com',
						          [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')

					messages.success(
					    request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect("index")
			messages.error(request, 'An invalid email has been entered.')
	password_reset_form = UserPasswordResetForm()
	return render(request, 'registration/password_reset_form.html', {"password_reset_form": password_reset_form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            clear_data = form.cleaned_data
            user = authenticate(request, 
                                username = clear_data['username'], 
                                password = clear_data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return HttpResponse('Verify your account.')
            else:
                return render(request, 'registration/login.html', { 'login_form': form, 'error': True })
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', { 'login_form': form })

def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():

            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)

            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])

            # Save the user object
            new_user.save()
            Profile.objects.create(user=new_user)

            return render(request, 'account/register_done.html', {
                'new_user': new_user
            })
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {
        'user_form': user_form
    })
