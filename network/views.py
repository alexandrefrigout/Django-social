from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from network.models import Profile
from network.form import ProfileForm, UserForm
from relationships.models import RelationshipManager, RelationshipStatus
from django.core import serializers
from rest_framework import viewsets, generics, mixins
from network.serializers import UserSerializer, GroupSerializer, ProfileSerializer
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.views.generic.detail import DetailView
from rest_framework import status


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

@api_view(('GET',))
@permission_classes((IsAuthenticated, ))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def viewprofile(request, userid):
        if request.user.is_authenticated():
                pro = Profile.objects.get(user_id=userid)
                if request.accepted_renderer.format == 'html':
                        data = {'profile' : pro}
                        return Response(data, template_name='network/profile.html')
                serializer = ProfileSerializer(instance=pro)
                data = serializer.data
                return Response(data)



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

#C@login_required
#def searchuser(request):
#	#try:
#	chaine = request.GET['chaine']
#	UserResult = User.objects.filter(username__icontains=chaine)
#	print UserResult
#	ProfileResult = []
#	for us in UserResult:
#		if not us.is_superuser and us.is_active:
#			ProfileResult.append(Profile.objects.get(user=us))
#			#print dir(Profile.objects.get(user=us).profilepicture)
#			#print Profile.objects.get(user=us).profilepicture.name
#	print ProfileResult
#	return render(request, 'network/searchresult.html', {'profile' : ProfileResult, 'request' : request})
#	#except:
#	#	return StreamingHttpResponse({'Bad' : 'isBad'})


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

#implementation of the rest_framework api to be able to render html or JSon

#@csrf_exempt
def searchuser(request, chaine):
        p = Profile.objects.all().filter(user__username__icontains=chaine)
        d = serializers.serialize('json', p, use_natural_keys=True, fields=('user', 'gender'))
        return HttpResponse(d, content_type="application/json")

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@api_view(('DATA',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@permission_classes((AllowAny, ))
def list_profiles(request):
        ch = request.DATA.get('chaine')
        queryset = Profile.objects.all().filter(user__username__icontains=ch)

        if request.accepted_renderer.format == 'html':
                data = {'profile' : queryset, 'request' : request}
                return Response(data, template_name='network/searchresult.html')

        serializer = ProfileSerializer(instance=queryset, many=True)
        data = serializer.data
        return Response(data)


class ProfileDetailView(DetailView):
        model = Profile
        template_name = 'network/detailed_view.html'



@permission_classes((AllowAny, ))
class ProfileCreate(mixins.CreateModelMixin, generics.GenericAPIView):
        #serializer_class = ProfileSerializer
        serializer_class = UserSerializer
        print("Profile!!!")
        def post(self, request, *args, **kwargs):
                print(request.body)
                return self.create(request, *args, **kwargs)

@api_view(('POST',))
@permission_classes((AllowAny, ))
def profile_create(request):
        if request.method == 'POST':
                print(request)
                print("DATA USER")
                #data = {'user': request.POST.get('user'), 'email': request.POST.get('email'), 'password1': request.POST.get('password1'), 'password2': request.POST.get('password2')}
                data = {'username': request.POST.get('user')}
                print(data)
                serializer = UserSerializer(data=data)
                if serializer.is_valid():
                        print("Valid!!!")
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
