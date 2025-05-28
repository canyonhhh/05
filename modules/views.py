from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.http import Http404
from .models import Module
from .forms import ModuleForm
from django.http import HttpResponse
from .pdf import generate_module_pdf


def home(request):
    """Home page - shows user's modules if logged in"""
    if request.user.is_authenticated:
        modules = Module.objects.filter(user=request.user)
        return render(request, 'modules/home.html', {'modules': modules})
    return render(request, 'modules/home.html')


def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def module_list(request):
    """List all modules for the current user"""
    modules = Module.objects.filter(user=request.user)
    return render(request, 'modules/module_list.html', {'modules': modules})


@login_required
def module_detail(request, pk):
    """View a specific module"""
    module = get_object_or_404(Module, pk=pk)
    
    if module.user != request.user:
        raise Http404("Module not found")
    
    return render(request, 'modules/module_detail.html', {'module': module})


@login_required
def module_create(request):
    """Create a new module"""
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.user = request.user
            module.save()
            messages.success(request, 'Module created successfully!')
            return redirect('module_detail', pk=module.pk)
    else:
        form = ModuleForm()
    
    return render(request, 'modules/module_form.html', {
        'form': form,
        'title': 'Create New Module'
    })


@login_required
def module_edit(request, pk):
    """Edit an existing module"""
    module = get_object_or_404(Module, pk=pk)
    
    if module.user != request.user:
        raise Http404("Module not found")
    
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            messages.success(request, 'Module updated successfully!')
            return redirect('module_detail', pk=module.pk)
    else:
        form = ModuleForm(instance=module)
    
    return render(request, 'modules/module_form.html', {
        'form': form,
        'module': module,
        'title': f'Edit Module: {module.name}'
    })


@login_required
def module_delete(request, pk):
    """Delete a module"""
    module = get_object_or_404(Module, pk=pk)
    
    if module.user != request.user:
        raise Http404("Module not found")
    
    if request.method == 'POST':
        module.delete()
        messages.success(request, 'Module deleted successfully!')
        return redirect('module_list')
    
    return render(request, 'modules/module_confirm_delete.html', {'module': module})

@login_required
def module_pdf(request, pk):
    """Generate and download PDF for a module"""
    module = get_object_or_404(Module, pk=pk)
    
    if module.user != request.user:
        raise Http404("Module not found")
    
    pdf_content = generate_module_pdf(module)
    
    response = HttpResponse(pdf_content, content_type='application/pdf')
    filename = f"module_{module.code or module.id}_{module.name[:50]}.pdf"
    filename = "".join(c for c in filename if c.isalnum() or c in "._- ").strip()
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
