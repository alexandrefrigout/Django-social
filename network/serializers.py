from django.contrib.auth.models import User, Group
from network.models import Profile
from rest_framework import serializers

#class UserSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = User
#        fields = ('username',)
#
#class ProfileSerializer(serializers.HyperlinkedModelSerializer):
#    user = UserSerializer()
#    class Meta:
#       model = Profile
#       fields = ('user', 'city', 'gender', 'url')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class ProfileSerializer(serializers.ModelSerializer):
    url = serializers.URLField(source='abs_url', read_only=True)
    user = serializers.CharField(source='user_name', read_only=True)
    static = serializers.CharField(source='static_url', read_only=True)
    class Meta:
        model = Profile
        fields = ('user', 'city', 'gender', 'profilepicture', 'url', 'static')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
