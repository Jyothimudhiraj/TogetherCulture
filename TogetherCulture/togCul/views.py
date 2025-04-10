from datetime import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Benefits, CustomUser, AllEvents, Interests
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomUser,DigitalContent, RegisteredDigitalContent
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token   
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

# Create your views here.
@never_cache
def home(request):
    user_data = request.session.get('user_data', None)
    return render(request, "home.html", {"user_data": user_data})

@never_cache
def AdminLogin(request):
    return render(request, "AdminLogin.html")

@never_cache
def UserRegistration(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        interests = request.POST.getlist('interests')  # Get selected interests as a list

        # Validate that at least 3 interests are selected
        if len(interests) < 3:
            messages.error(request, "Please select at least 3 interests.")
            return render(request, 'UserRegistration.html')

        # Validate passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'UserRegistration.html')

        # Hash the password before saving
        hashed_password = make_password(password)

        # Save the user to the database
        user = CustomUser.objects.create(
            full_name=full_name,
            email=email,
            password=hashed_password,
            interests=interests  # Save interests as a JSON list
        )

        messages.success(request, "Registration successful!")
        return redirect('home')

    return render(request, 'UserRegistration.html')

def login_view(request):
    if request.method == "POST":
        Useremail = request.POST.get('email')
        password = request.POST.get('member-login-password')

        try:
            user = CustomUser.objects.get(email=Useremail)
            if check_password(password, user.password):  # Verify hashed password
                # Store user data in the session
                request.session['user_data'] = {
                    'full_name': user.full_name,
                    'email': user.email,
                    'membershipstatus': user.membershipStatus,
                    'membership': user.membershipType,
                    'interests': user.interests,  # Fetch interests from the database
                    'benefits': ["Benefit 1", "Benefit 2", "Benefit 3"]  # Example benefits
                }
                print("Session Data After Login:", request.session['user_data'])
                return redirect(reverse('BenifitsAndInterests'))  # Redirect to the page
            else:
                messages.error(request, "Invalid password")
        except CustomUser.DoesNotExist:
            messages.error(request, "User with this email doesn't exist")

    return render(request, "home.html")


@never_cache
def logout_view(request):
    request.session.flush()
    print("User logged out")
    return redirect(reverse('home'))

@never_cache
def EventsListing(request):
    return render(request, "event-listing.html")

def BenifitsandInterests(request):
    # Fetch user data from the session
    user_data = request.session.get('user_data')
    if not user_data:
        return redirect('login')  # Redirect to login if the user is not logged in

    # Fetch user interests and benefits from the session
    user_interests = user_data.get('interests', [])
    user_benefits = user_data.get('benefits', [])

    # Debugging: Print the data to the console
    print("User Interests:", user_interests)
    print("User Benefits:", user_benefits)

    return render(request, 'BenifitsandInterests.html', {
        'user_Interests': user_interests,
        'user_Benifits': user_benefits
    })

@never_cache
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:  # Ensure only superusers can log in
            login(request, user)
            print("Admin login Successfull")
            return redirect('AdminDashboard')  # Redirect to your admin panel page
        else:
            print("Not logging in")
            messages.error(request, "Invalid credentials or not an admin.")
    
    return render(request, 'AdminLogin.html')


@never_cache
def AdminDashboard(request):
    approvedUsers = CustomUser.objects.filter(membershipStatus = 2 )
    pendingUsers = CustomUser.objects.filter(membershipStatus = 1)
    content = {
        'Total_Members': approvedUsers.count(),
        'Pending_Users': pendingUsers
    }
    return render(request, 'AdminDashboard.html', content)

@never_cache
def update_membership(request):
    user_id = request.session['user_data']['email']  # Get the user ID from the session
    print(user_id)
    try:
        # Get the user object using the session ID
        user = CustomUser.objects.get(email=user_id)
        print(user)
    except CustomUser.DoesNotExist:
        # If the user doesn't exist in the database, handle the error
        print("exception")
        return redirect('home')  # Replace with an actual error page or message
    
    if request.method == 'POST':
        # Get the membership status and membership type from the form
        membership_status = 1
        membership_type = request.POST.get('Choice')
        print(membership_type)

        # Update the user's membership status and membership type
        user.membershipStatus = membership_status
        user.membershipType = membership_type
        print("details updated")
        # Save the updated user object
        user.save()

        # Redirect to the profile page or another page where the user can see the updated info
        return redirect(reverse('home'))  # Replace 'profile' with your actual profile page URL name

    # Render the form with the current membership data
    return render(request, 'home.html')

@never_cache
def process_membership(request, email):
    user = CustomUser.objects.get(email= email)
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            user.membershipStatus = 2
        elif action == 'reject':
            user.membershipStatus = 0
    user.save()
    return redirect(reverse('AdminDashboard'))



@csrf_exempt
def add_event_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            event_name = data.get('event_name')
            event_description = data.get('description')

            if not event_name or not event_description:
                return JsonResponse({'error': 'Event name and description are required.'}, status=400)

            AllEvents.objects.create(name=event_name, description=event_description)
            return JsonResponse({'message': 'Event added successfully!'}, status=201)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': 'An error occurred while adding the event.'}, status=500)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

from django.shortcuts import render
from django.db.models import Q
from .models import CustomUser

def search_members(request):
    query = request.GET.get('query', '')
    members = CustomUser.objects.filter(
        Q(full_name__icontains=query) | Q(email__icontains=query)
    ) if query else CustomUser.objects.all()

    return render(request, 'AdminDashboard.html', {
        'members': members,
        'Total_Members': members.count(),
    })

def profile(request):
    # Check if user is logged in
    if not request.session.get('user_data'):
        return redirect('login')  # Redirect to login if not logged in

    # Fetch user data from session
    user_data = request.session.get('user_data', {})
    return render(request, 'profile.html', {'user_data': user_data})

def digital_content(request):
    user_data = request.session.get('user_data')
    if not user_data:
        return redirect('login')  # Redirect to login if not logged in

    digital_contents = DigitalContent.objects.all()
    registered_contents = RegisteredDigitalContent.objects.select_related('digitalContent', 'user')
    return render(request, 'DigitalContent.html', {
        'digital_contents': digital_contents,
        'registered_contents': registered_contents,
    })

def add_digital_content(request):
    if request.method == 'POST':
        content_name = request.POST.get('contentName')
        content_description = request.POST.get('contentDescription')
        access_by = request.POST.get('accessBy')
        image = request.FILES.get('image')

        DigitalContent.objects.create(
            contentName=content_name,
            contentDescription=content_description,
            accessBy=access_by,
            image=image
        )
        return redirect('DigitalContent')  # Use the correct URL name here

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def register_digital_content(request, content_id):
    if request.method == 'POST':
        # Fetch the logged-in user from the session
        user_data = request.session.get('user_data')
        if not user_data:
            return JsonResponse({'error': 'User not logged in.'}, status=403)

        # Fetch the user object using the email from the session
        user = CustomUser.objects.get(email=user_data['email'])

        # Fetch the digital content
        digital_content = get_object_or_404(DigitalContent, id=content_id)

        # Check if the user has already registered for this content
        if RegisteredDigitalContent.objects.filter(user=user, digitalContent=digital_content).exists():
            return JsonResponse({'error': 'Already registered for this content.'}, status=400)

        # Create a new registration entry
        RegisteredDigitalContent.objects.create(user=user, digitalContent=digital_content)

        # Debugging: Confirm creation
        print("Registered Digital Content Created:", user, digital_content)

        return JsonResponse({'message': 'Registration successful!'}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
def view_digital_content(request):
    digital_contents = DigitalContent.objects.all()
    registered_content_ids = []
    registered_contents = []

    # Use session data to fetch the logged-in user
    user_data = request.session.get('user_data')
    if user_data:
        user = CustomUser.objects.get(email=user_data['email'])  # Fetch the user using session data
        registered_contents = RegisteredDigitalContent.objects.filter(user=user)
        registered_content_ids = registered_contents.values_list('digitalContent_id', flat=True)

        # Debugging: Check fetched data
        print("Registered Contents with Descriptions:", list(registered_contents.values('digitalContent__contentDescription')))

    return render(request, 'DigitalContent.html', {
        'digital_contents': digital_contents,
        'registered_contents': registered_contents,
        'registered_content_ids': registered_content_ids,
    })