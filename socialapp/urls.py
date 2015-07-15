from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login
from network.form import UserRegistrationForm, UserLoginForm
from network.regbackend import ProfileBackend
from network import views
admin.autodiscover()

urlpatterns = patterns('',
	url(r'', include('network.urls')),
	url(r'^accounts/register/$',
			ProfileBackend.as_view(form_class = UserRegistrationForm), name='registration_register'),
	url(r'^accounts/login', 
			'django.contrib.auth.views.login',{'template_name':'registration/login.html', 'authentication_form':UserLoginForm}),
	url(r'^accounts/profile', views.profile, ),
	url(r'^accounts/editprofile/(\w+)', views.editProfile, ),
	url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
