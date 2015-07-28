import os
from django.contrib.auth.models import User
from relationships.models import RelationshipManager, RelationshipStatus
from django import template

register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(value.file.name)


@register.filter
def get_nb_friends(value):
	user = User.objects.get(username=str(value))
	status = RelationshipStatus.objects.by_slug('following')
	return value.relationships.get_relationships(status=status, accepted=True).count()

@register.filter
def is_your_rel(value, to_user):
	user = User.objects.get(username=str(value))
	to_user = User.objects.get(username=str(to_user))
	status = RelationshipStatus.objects.by_slug('following')
	return user.relationships.exists(user, to_user)
	
