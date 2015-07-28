from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, StreamingHttpResponse
from network.models import Profile
from network.form import ProfileForm, UserForm
from relationships.models import RelationshipManager, RelationshipStatus


@login_required
def profile(request):
	if request.user.is_authenticated():
		user = User.objects.get(username=str(request.user))
		print user
		profile = Profile.objects.get(user_id = user.id)
		status = RelationshipStatus.objects.by_slug('following')	
		num_rel = user.relationships.get_relationships(status=status, accepted=True).count()
		#return StreamingHttpResponse('%s est connecte'% str(user))
		return render(request, 'network/profile.html', {'profile' : profile, 'relnumber' : num_rel})

@login_required
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
                        	return render(request, 'network/editprofile.html', {'profile' : form, 'user' : userform, 'photoprofile' : initialprofile})
                                #return StreamingHttpResponse({'Bad' : 'isBad'})


                else:
                        print "NOT POSTED"
                        userform = UserForm(instance=user)
                        form = ProfileForm(instance=initialprofile)

                        return render(request, 'network/editprofile.html', {'profile' : form, 'user' : userform, 'photoprofile' : initialprofile})

	else:
		return HttpResponseRedirect('/accounts/login')

@login_required
def searchuser(request):
	#try:
	chaine = request.GET['chaine']
	UserResult = User.objects.filter(username__icontains=chaine)
	print UserResult
	ProfileResult = []
	for us in UserResult:
		if not us.is_superuser and us.is_active:
			ProfileResult.append(Profile.objects.get(user=us))
			#print dir(Profile.objects.get(user=us).profilepicture)
			#print Profile.objects.get(user=us).profilepicture.name
	print ProfileResult
	return render(request, 'network/searchresult.html', {'profile' : ProfileResult, 'request' : request})
	#except:
	#	return StreamingHttpResponse({'Bad' : 'isBad'})

#@login_required
#def FollowUser(request, user):
#	try:
#		TargetUser = User.objects.get(id=user)
#		print TargetUser.pk, request.user.pk
#		if TargetUser.pk is not request.user.pk:
#			request.user.relationships.add(TargetUser)
#			return StreamingHttpResponse({'Ok' : 'isOK'})
#		else:
#			return StreamingHttpResponse({'Bad' : 'isBad'})
#	except:
#		return StreamingHttpResponse({'Bad' : 'isBad'})
#	
