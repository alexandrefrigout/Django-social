from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login
from network.form import UserRegistrationForm, UserLoginForm
from network.regbackend import ProfileBackend
from network import views

urlpatterns = patterns('',
	url(r'', include('network.urls')),
	url(r'^accounts/register/$',
			ProfileBackend.as_view(form_class = UserRegistrationForm), name='registration_register'),
	url(r'^accounts/login', 
			'django.contrib.auth.views.login',{'template_name':'registration/login.html', 'authentication_form':UserLoginForm}),
	url(r'^accounts/profile', views.profile, ),
	url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
