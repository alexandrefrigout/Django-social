from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from network.models import Profile


@login_required
def profile(request):
	if request.user.is_authenticated():
		user = User.objects.get(username=str(request.user))
		profile = Profile.objects.get(user_id = user.id)
		#return HttpResponse('%s est connecte'% str(user))
		return render(request, 'network/profile.html', {'profile' : profile})

