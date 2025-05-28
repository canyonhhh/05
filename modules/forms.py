from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, HTML
from .models import Module


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = [
            'name', 'code', 'coordinating_instructor', 'other_instructors',
            'department', 'faculty', 'university', 'study_level', 'module_type',
            'implementation_form', 'semester', 'language', 'prerequisites',
            'credits', 'total_workload', 'contact_hours', 'self_study_hours',
            'general_competencies', 'subject_competencies'
        ]
        
        widgets = {
            'other_instructors': forms.Textarea(attrs={'rows': 3}),
            'prerequisites': forms.Textarea(attrs={'rows': 3}),
            'general_competencies': forms.Textarea(attrs={'rows': 4}),
            'subject_competencies': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Basic Information',
                Row(
                    Column('name', css_class='col-md-8'),
                    Column('code', css_class='col-md-4'),
                ),
                Row(
                    Column('coordinating_instructor', css_class='col-md-6'),
                    Column('department', css_class='col-md-6'),
                ),
                Row(
                    Column('faculty', css_class='col-md-6'),
                    Column('university', css_class='col-md-6'),
                ),
                'other_instructors',
            ),
            Fieldset(
                'Study Details',
                Row(
                    Column('study_level', css_class='col-md-4'),
                    Column('module_type', css_class='col-md-4'),
                    Column('implementation_form', css_class='col-md-4'),
                ),
                Row(
                    Column('semester', css_class='col-md-6'),
                    Column('language', css_class='col-md-6'),
                ),
                'prerequisites',
            ),
            Fieldset(
                'Workload',
                Row(
                    Column('credits', css_class='col-md-3'),
                    Column('total_workload', css_class='col-md-3'),
                    Column('contact_hours', css_class='col-md-3'),
                    Column('self_study_hours', css_class='col-md-3'),
                ),
            ),
            Fieldset(
                'Competencies',
                'general_competencies',
                'subject_competencies',
            ),
            Submit('submit', 'Save Module', css_class='btn btn-primary btn-lg')
        )
