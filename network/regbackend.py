from registration.backends.default.views import RegistrationView


class ProfileBackend(RegistrationView):
	
	def register(self,request, **kwargs):
		from network.models import Profile
		user = super(ProfileBackend, self).register(request, **kwargs)
		user.save()
		profile = Profile.objects.create(
									user=user, gender=kwargs['gender'])
		profile.save()

	def get_form_class(self, request):

		from network.form import UserRegistrationForm
		return UserRegistrationForm
