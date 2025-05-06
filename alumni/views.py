from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import AlumniProfile, School, Event
from .forms import UserRegisterForm, AlumniProfileForm, CustomLoginForm, SchoolForm, AlumniStatusForm
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect


class CustomLoginView(LoginView):
    """Custom login view with enhanced form"""
    form_class = CustomLoginForm
    template_name = 'alumni/login.html'

def custom_logout(request):
    """Custom logout view that accepts GET requests and redirects to home page"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def register(request):
    """View for user registration"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # The profile is automatically created by the signal, so we don't need this line:
            # AlumniProfile.objects.create(user=user)
            messages.success(request, f'Your account has been created! You can now log in.')
            return redirect('alumni:login')
    else:
        form = UserRegisterForm()
    return render(request, 'alumni/register.html', {'form': form})

@login_required
def profile(request):
    """View for user's own profile"""
    profile = get_object_or_404(AlumniProfile, user=request.user)
    
    if request.method == 'POST':
        form = AlumniProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('alumni:profile')
    else:
        form = AlumniProfileForm(instance=profile)
    
    return render(request, 'alumni/profile.html', {
        'profile': profile,
        'form': form
    })


class AlumniListView(ListView):
    """View for listing alumni profiles"""
    model = AlumniProfile
    template_name = 'alumni/alumni_list.html'
    context_object_name = 'alumni'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = AlumniProfile.objects.filter(status='registered')  # Only show registered alumni
        
        # Filter by school if specified
        school_id = self.request.GET.get('school')
        if school_id:
            queryset = queryset.filter(school_id=school_id)
        
        # Filter by search query if provided
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(major__icontains=query) |
                Q(degree__icontains=query) |
                Q(current_company__icontains=query) |
                Q(job_title__icontains=query)
            )
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schools'] = School.objects.all()
        context['selected_school'] = self.request.GET.get('school')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class AlumniDetailView(DetailView):
    """View for individual alumni profile details"""
    model = AlumniProfile
    template_name = 'alumni/alumni_detail.html'
    context_object_name = 'alumni'
    
    def get_queryset(self):
        # Only show registered alumni to the public
        return AlumniProfile.objects.filter(status='registered')
    
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            return super().get(request, *args, **kwargs)
        except:
            messages.error(request, "The requested profile doesn't exist or is not publicly available.")
            return redirect('alumni:alumni_list')


class SchoolListView(ListView):
    """View for listing schools"""
    model = School
    template_name = 'alumni/school_list.html'
    context_object_name = 'schools'


class SchoolDetailView(DetailView):
    """View for school details with associated alumni"""
    model = School
    template_name = 'alumni/school_detail.html'
    context_object_name = 'school'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Only show registered alumni in this school
        context['alumni'] = AlumniProfile.objects.filter(
            school=self.object,
            status='registered'
        )
        return context


class EventListView(ListView):
    """View for listing events"""
    model = Event
    template_name = 'alumni/event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        return Event.objects.all().order_by('date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_events'] = Event.objects.filter(date__gte=timezone.now()).order_by('date')
        context['past_events'] = Event.objects.filter(date__lt=timezone.now()).order_by('-date')
        return context


class EventDetailView(DetailView):
    """View for event details"""
    model = Event
    template_name = 'alumni/event_detail.html'
    context_object_name = 'event'


@login_required
def event_register(request, pk):
    """View for event registration"""
    event = get_object_or_404(Event, pk=pk)
    profile = get_object_or_404(AlumniProfile, user=request.user)
    
    if not event.can_register:
        messages.error(request, "Registration is not available for this event.")
        return redirect('alumni:event_detail', pk=event.pk)
    
    if profile in event.attendees.all():
        event.attendees.remove(profile)
        messages.success(request, f"You've been removed from {event.title}.")
    else:
        event.attendees.add(profile)
        messages.success(request, f"You've registered for {event.title}.")
    
    return redirect('alumni:event_detail', pk=event.pk)


# Admin-only views
class IsAdminMixin(UserPassesTestMixin):
    """Mixin to check if user is an admin"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


@method_decorator(login_required, name='dispatch')
class AdminDashboardView(IsAdminMixin, ListView):
    """Admin dashboard view"""
    model = AlumniProfile
    template_name = 'alumni/admin/dashboard.html'
    context_object_name = 'alumni'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_alumni'] = AlumniProfile.objects.count()
        context['registered_alumni'] = AlumniProfile.objects.filter(status='registered').count()
        context['applied_alumni'] = AlumniProfile.objects.filter(status='applied').count()
        context['schools'] = School.objects.all()
        context['events'] = Event.objects.all()
        context['pending_approvals'] = AlumniProfile.objects.filter(status='applied')
        return context


@method_decorator(login_required, name='dispatch')
class AlumniStatusUpdateView(IsAdminMixin, UpdateView):
    """View for admins to update alumni status"""
    model = AlumniProfile
    form_class = AlumniStatusForm
    template_name = 'alumni/admin/alumni_status_update.html'
    success_url = reverse_lazy('alumni:admin_dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Status updated successfully for {self.object.user.get_full_name()}.")
        return response


@method_decorator(login_required, name='dispatch')
class SchoolCreateView(IsAdminMixin, CreateView):
    """View for admins to create a new school"""
    model = School
    form_class = SchoolForm
    template_name = 'alumni/admin/school_form.html'
    success_url = reverse_lazy('alumni:admin_dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"School '{self.object.name}' created successfully.")
        return response


@method_decorator(login_required, name='dispatch')
class SchoolUpdateView(IsAdminMixin, UpdateView):
    """View for admins to update a school"""
    model = School
    form_class = SchoolForm
    template_name = 'alumni/admin/school_form.html'
    success_url = reverse_lazy('alumni:admin_dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"School '{self.object.name}' updated successfully.")
        return response


@method_decorator(login_required, name='dispatch')
class EventCreateView(IsAdminMixin, CreateView):
    """View for admins to create a new event"""
    model = Event
    fields = ['title', 'description', 'date', 'location', 'image', 
              'registration_required', 'registration_deadline']
    template_name = 'alumni/admin/event_form.html'
    success_url = reverse_lazy('alumni:admin_dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Event '{self.object.title}' created successfully.")
        return response


@method_decorator(login_required, name='dispatch')
class EventUpdateView(IsAdminMixin, UpdateView):
    """View for admins to update an event"""
    model = Event
    fields = ['title', 'description', 'date', 'location', 'image',
              'registration_required', 'registration_deadline']
    template_name = 'alumni/admin/event_form.html'
    success_url = reverse_lazy('alumni:admin_dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Event '{self.object.title}' updated successfully.")
        return response