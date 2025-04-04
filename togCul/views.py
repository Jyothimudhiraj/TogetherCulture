from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import MemberForm
from .models import Member
from django.contrib.auth.models import User  #



# Main homepage
def home(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = MemberForm()
    return render(request, 'home.html', {'form': form})

# Events
def event_listing(request):
    return render(request, 'event-listing.html')

def event_detail(request):
    return render(request, 'event-detail.html')

# Admin panel main dashboard template
def dashboard_view(request):
    return render(request, 'pages/dashboard.html')

# Admin action
def approve_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.approved = True
    member.save()
    return redirect('admin-dashboard')

def dashboard_view(request):
    total_members = User.objects.count()  # Count all users
    return render(request, 'pages/dashboard.html', {'total_members': total_members})


def page_notifications(request):
    return render(request, 'pages/notifications.html')


def page_rtl(request):
    return render(request, 'pages/rtl.html')


def page_tables(request):
    return render(request, 'pages/tables.html')

def page_virtual(request):
    return render(request, 'pages/eventadd.html')





from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .forms import EventForm
from datetime import date
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from .forms import EventForm
from datetime import date

def add_event(request):
    query = request.GET.get('q')  # Handle search functionality
    if query:
        events = Event.objects.filter(name__icontains=query)  # Filter events by name
    else:
        events = Event.objects.all()  # Show all events if no query is provided

    today = date.today()  # Get the current date

    if request.method == 'POST':  # Handle form submission
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()  # Save the event to the database
            return redirect('eventadd')  # Redirect to the same page after saving
    else:
        form = EventForm()

    return render(request, 'pages/eventadd.html', {'form': form, 'events': events, 'today': today})
# Edit Event
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('eventadd')
    else:
        form = EventForm(instance=event)
    return render(request, 'pages/eventedit.html', {'form': form, 'event': event})

# Delete Event
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('eventadd')