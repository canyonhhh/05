from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Module(models.Model):
    """Main module model representing a university course module"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modules')
    
    name = models.CharField(max_length=200, verbose_name="Module Name")
    code = models.CharField(max_length=50, blank=True, verbose_name="Module Code")
    
    coordinating_instructor = models.CharField(max_length=100, verbose_name="Coordinating Instructor")
    other_instructors = models.TextField(blank=True, verbose_name="Other Instructors")
    
    department = models.CharField(max_length=100, verbose_name="Department")
    faculty = models.CharField(max_length=100, verbose_name="Faculty")
    university = models.CharField(max_length=100, default="Vilnius University", verbose_name="University")
    
    STUDY_LEVEL_CHOICES = [
        ('first', 'First Level (Bachelor)'),
        ('second', 'Second Level (Master)'),
        ('third', 'Third Level (Doctoral)'),
    ]
    
    MODULE_TYPE_CHOICES = [
        ('compulsory', 'Compulsory'),
        ('elective', 'Elective'),
        ('free_elective', 'Free Elective'),
    ]
    
    IMPLEMENTATION_FORM_CHOICES = [
        ('classroom', 'Classroom'),
        ('distance', 'Distance Learning'),
        ('mixed', 'Mixed'),
    ]
    
    LANGUAGE_CHOICES = [
        ('lithuanian', 'Lithuanian'),
        ('english', 'English'),
        ('other', 'Other'),
    ]
    
    study_level = models.CharField(max_length=20, choices=STUDY_LEVEL_CHOICES, verbose_name="Study Level")
    module_type = models.CharField(max_length=20, choices=MODULE_TYPE_CHOICES, verbose_name="Module Type")
    implementation_form = models.CharField(max_length=20, choices=IMPLEMENTATION_FORM_CHOICES, verbose_name="Implementation Form")
    semester = models.CharField(max_length=50, verbose_name="Semester")
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, verbose_name="Language")
    
    prerequisites = models.TextField(blank=True, verbose_name="Prerequisites")
    
    credits = models.IntegerField(verbose_name="Credits")
    total_workload = models.IntegerField(verbose_name="Total Student Workload (hours)")
    contact_hours = models.IntegerField(verbose_name="Contact Hours")
    self_study_hours = models.IntegerField(verbose_name="Self-study Hours")
    
    general_competencies = models.TextField(verbose_name="General Competencies")
    subject_competencies = models.TextField(verbose_name="Subject-specific Competencies")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Module"
        verbose_name_plural = "Modules"
    
    def __str__(self):
        return f"{self.name} ({self.code})" if self.code else self.name
    
    def get_absolute_url(self):
        return reverse('module_detail', kwargs={'pk': self.pk})


class LearningOutcome(models.Model):
    """Learning outcomes for a module"""
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='learning_outcomes')
    description = models.TextField(verbose_name="Learning Outcome Description")
    competency_code = models.CharField(max_length=20, blank=True, verbose_name="Competency Code")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.name} - Outcome {self.order + 1}"


class Topic(models.Model):
    """Course topics with hour breakdown"""
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=300, verbose_name="Topic Title")
    lecture_hours = models.IntegerField(default=0, verbose_name="Lecture Hours")
    consultation_hours = models.IntegerField(default=0, verbose_name="Consultation Hours")
    seminar_hours = models.IntegerField(default=0, verbose_name="Seminar Hours")
    practical_hours = models.IntegerField(default=0, verbose_name="Practical Hours")
    lab_hours = models.IntegerField(default=0, verbose_name="Laboratory Hours")
    consultation_practical_hours = models.IntegerField(default=0, verbose_name="Consultation during Practicals")
    self_study_hours = models.IntegerField(default=0, verbose_name="Self-study Hours")
    assignments = models.TextField(blank=True, verbose_name="Assignments")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.name} - {self.title}"
    
    @property
    def total_contact_hours(self):
        return (self.lecture_hours + self.consultation_hours + self.seminar_hours + 
                self.practical_hours + self.lab_hours + self.consultation_practical_hours)


class Assessment(models.Model):
    """Assessment methods and weights"""
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='assessments')
    method = models.CharField(max_length=100, verbose_name="Assessment Method")
    weight_percentage = models.IntegerField(verbose_name="Weight (%)")
    timing = models.CharField(max_length=100, verbose_name="Assessment Timing")
    criteria = models.TextField(verbose_name="Assessment Criteria")
    
    class Meta:
        ordering = ['-weight_percentage']
    
    def __str__(self):
        return f"{self.module.name} - {self.method} ({self.weight_percentage}%)"


class Literature(models.Model):
    """Required and additional literature"""
    LITERATURE_TYPE_CHOICES = [
        ('required', 'Required Literature'),
        ('additional', 'Additional Literature'),
    ]
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='literature')
    literature_type = models.CharField(max_length=20, choices=LITERATURE_TYPE_CHOICES, verbose_name="Literature Type")
    author = models.CharField(max_length=200, verbose_name="Author")
    year = models.IntegerField(verbose_name="Publication Year")
    title = models.CharField(max_length=300, verbose_name="Title")
    volume_or_issue = models.CharField(max_length=100, blank=True, verbose_name="Volume/Issue")
    publisher_or_url = models.CharField(max_length=300, verbose_name="Publisher/Location or URL")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['literature_type', 'order']
    
    def __str__(self):
        return f"{self.author} ({self.year}) - {self.title}"
