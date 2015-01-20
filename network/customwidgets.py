from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput, CheckboxInput

class AdvancedFileInput(ClearableFileInput):

    def __init__(self, *args, **kwargs):

        self.url_length = kwargs.pop('url_length',30)
        self.preview = kwargs.pop('preview',True)
        self.image_width = kwargs.pop('image_width',200)
        super(AdvancedFileInput, self).__init__(*args, **kwargs)
	
    def render(self, name, value, attrs=None,):
        substitutions = {}
        template = u'%(input)s<br />'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):

            template = '%(input)s<br />'

        return mark_safe(template % substitutions)

