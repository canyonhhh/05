from django.contrib import admin
from .models import Module, LearningOutcome, Topic, Assessment, Literature


class LearningOutcomeInline(admin.TabularInline):
    model = LearningOutcome
    extra = 1


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1


class AssessmentInline(admin.TabularInline):
    model = Assessment
    extra = 1


class LiteratureInline(admin.TabularInline):
    model = Literature
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'user', 'credits', 'study_level', 'updated_at']
    list_filter = ['study_level', 'module_type', 'language', 'created_at']
    search_fields = ['name', 'code', 'coordinating_instructor']
    inlines = [LearningOutcomeInline, TopicInline, AssessmentInline, LiteratureInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set user on creation
            obj.user = request.user
        super().save_model(request, obj, form, change)
