from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models import Project, Template, ProjectCategory, ProjectCategoryMembership
from .fields import PopcornJSONField


class ProjectForm(forms.Form):
    """Form used to validate the data sent through the API."""
    name = forms.CharField()
    data = PopcornJSONField()
    template = forms.ModelChoiceField(queryset=Template.live.all(),
                                      empty_label=None,
                                      to_field_name='slug')


class ProjectEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ProjectEditForm, self).__init__(*args, **kwargs)
        queryset = (ProjectCategory.objects
                    .filter(projectcategorymembership__user=user,
                            projectcategorymembership__status=ProjectCategoryMembership.APPROVED))
        self.has_categories = True if queryset else False
        self.fields.update({
            'categories': forms.ModelMultipleChoiceField(queryset=queryset,
                                                         required=False,
                                                         widget=CheckboxSelectMultiple)
                                                         })

    class Meta:
        model = Project
        fields = ('name', 'description', 'thumbnail','is_shared', 'is_forkable',
                  'status', 'categories')


class ExternalProjectEditForm(ProjectEditForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'is_shared', 'status', 'categories')


class ProjectSubmissionForm(forms.ModelForm):
    name = forms.CharField()
    url = forms.URLField()
    thumbnail = forms.ImageField(required=False)

    class Meta:
        model = Project
        fields = ('name', 'description', 'url', 'thumbnail')
