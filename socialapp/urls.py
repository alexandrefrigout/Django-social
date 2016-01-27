from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import login
from network.form import UserRegistrationForm, UserLoginForm
from network.regbackend import ProfileBackend
from network import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profile', views.ProfileViewSet)
router.register(r'groups', views.GroupViewSet)


admin.autodiscover()

urlpatterns = patterns('',
        url(r'net/', include('network.urls')),
        url(r'^accounts/register/$',
                        ProfileBackend.as_view(form_class = UserRegistrationForm), name='registration_register'),
        url(r'^accounts/login', 
                        'django.contrib.auth.views.login',{'template_name':'registration/login.html', 'authentication_form':UserLoginForm}),
        url(r'^accounts/profile', views.profile, ),
        url(r'^accounts/editprofile/(\w+)', views.editProfile, ),
        url(r'^accounts/', include('registration.backends.default.urls')),
        #url(r'^net/searchuser/(\w+)', views.searchuser),
        url(r'^net/searchuser/', views.list_profiles),
        #url(r'^searchuser/', views.searchuser),
#       url(r'follow/(\w+)$', views.FollowUser),
        url(r'relationships/', include('relationships.urls')),
        url(r'viewprofile/(\d+)', views.viewprofile, name='viewprofile'),
        url(r'^', include(router.urls)),
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

        url(r'^detail/(?P<pk>\d+)', views.ProfileDetailView.as_view(), name='detailed-view'),

        url(r'reg/', views.ProfileCreate.as_view(), name='create-profile'),

        url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
