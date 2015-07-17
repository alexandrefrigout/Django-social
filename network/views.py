from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from network.models import Profile
from network.form import ProfileForm, UserForm


@login_required
def profile(request):
	if request.user.is_authenticated():
		user = User.objects.get(username=str(request.user))
		profile = Profile.objects.get(user_id = user.id)
		#return HttpResponse('%s est connecte'% str(user))
		return render(request, 'network/profile.html', {'profile' : profile})


def editProfile(request, userid):
        if request.user.is_authenticated() and User.objects.get(username=str(request.user)) == User.objects.get(id=userid):
                user = User.objects.get(id=userid)
                initialprofile = Profile.objects.get(user_id=user.id)

                if request.method == 'POST':
                        print "POSTED"
                        print request.FILES
                        userform = UserForm(request.POST, instance=user)
                        form = ProfileForm(request.POST, request.FILES, instance=initialprofile)

                        if form.is_valid() and userform.is_valid():
                                userform.save(commit=True)
                                form.save(commit=True)
                                return HttpResponseRedirect('/accounts/profile/'+str(user.id))
                        else:
                                print userform.errors
                                print form.errors
                                return HttpResponse({'Bad' : 'isBad'})


                else:
                        print "NOT POSTED"
                        userform = UserForm(instance=user)
                        form = ProfileForm(instance=initialprofile)

                        return render(request, 'network/editprofile.html', {'profile' : form, 'user' : userform, 'photoprofile' : initialprofile})

